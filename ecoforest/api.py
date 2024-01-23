import logging
from http import HTTPStatus
from typing import Any, List, Tuple
import httpx

from ecoforest.consts import (
    URL_CGI,
    LOCAL_TIMEOUT, ANALOGUE_READINGS_MAPPINGS
)
from ecoforest.exceptions import EcoforestAuthenticationRequired, EcoforestConnectionError, EcoforestError

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

# TODO: No more debug
_LOGGER.setLevel(logging.DEBUG)

_LOGGER.debug('init')


def log_debug(log_string: str) -> None:
    if _LOGGER.isEnabledFor(logging.DEBUG):
        _LOGGER.debug(log_string)

class EcoforestApi:
    """Class for communicating with an ecoforest device."""

    def __init__(
            self,
            host: str,
            auth: httpx.BasicAuth | None = None,
            client: httpx.AsyncClient | None = None,
            timeout: float | httpx.Timeout | None = None,
    ) -> None:
        self._host = host
        self._auth = auth
        # TODO - Needed?
        # We use our own httpx client session so we can disable SSL verification,
        # the device use self-signed SSL certs.
        self._timeout = timeout or LOCAL_TIMEOUT
        self._client = client or httpx.AsyncClient(
            base_url=self._host, verify=False
        )  # nosec



    async def _request(self, data: dict[str, Any] | None = None) -> dict[str, str]:
        """Make a request to the device."""
        log_debug(f"Sending POST to {URL_CGI} with data {data}")

        try:
            response = await self._client.post(
                URL_CGI,
                auth=self._auth,
                timeout=self._timeout,
                data=data,
            )
            response.raise_for_status()
        except httpx.TimeoutException as error:
            raise EcoforestConnectionError(
                "Timeout occurred while connecting to the device."
            ) from error
        except httpx.HTTPError as error:
            if error.response.status_code in (
                    HTTPStatus.UNAUTHORIZED,
                    HTTPStatus.FORBIDDEN,
            ):
                raise EcoforestAuthenticationRequired(
                    error.response.status_code
                ) from error
            raise EcoforestConnectionError(
                "Error occurred while communicating with device."
            ) from error

        parsed = self._parse(response.text)

        log_debug(f"Received from POST with data {parsed}")

        return parsed

    async def make_test_request(self):
        # 2002 = geo_get_reg
        return await self._request(data={"idOperacion": 2002, "dir": 161, "num": 5})

    async def make_read_operation_request(self, id_operation: int, specified_dir: int, num: int) -> dict:
        return await self._request(data={"idOperacion": id_operation, "dir": specified_dir, "num": num})

    @staticmethod
    def _parse(response: str) -> dict[str, str]:
        """Parse request data and return as dictionary."""

        log_debug(response)
        reply = {}
        # discard last line ?
        for l in response.split("\n")[:-1]:
            for e in l.split("&"):
                pair = e.split("=")
                if len(pair) == 2:
                    reply[pair[0]] = pair[1]
                elif len(pair) == 1:
                    # Probably got the remaining 'raw' values
                    reply['raw_data'] = reply.get("raw_data", []) + [e]
        reply["error_check"] = response.split("\n")[-1]

        # Remove all white spaces from bad response from ecoforest ...
        reply = {x.translate({32: None}): y for x, y in reply.items()}
        log_debug(f'{reply = }')
        return reply


class EcoGeo25100:
    GEO_GET_BIT = 2001
    GEO_GET_NUM = 2002

    def __init__(self, api: EcoforestApi):
        self.api = api
        self.digitals = [0] * 268
        self.integers = [0] * 163
        self.analogues = [0.0] * 228

    @staticmethod
    def _translate_values(base: int, source_values: List[Any], destination: List[Any], translate_ranges: List[Tuple[int, int]]):
        for start, stop in translate_ranges:
            for i in range(start, stop):
                destination[base+i] = source_values[i]

    @staticmethod
    def _map_digital_values(input_values: List[str]) -> List[int]:
        return list(map(lambda x: 1 if x == "1" else 0, input_values))

    async def read_translate_digitals(self) -> List[int]:
        di1 = await self.api.make_read_operation_request(self.GEO_GET_BIT, 24, 70)
        err_value = int(di1.get('error_check', -1))
        if err_value < 0:
            raise EcoforestError(f"Got error value: {err_value}")
        values = self._map_digital_values(di1.get('raw_data', []))
        self._translate_values(24, values, self.digitals, [
            (0, 1), (18, 25), (35, 48), (59, 62), (69, 70)
        ])

        di2 = await self.api.make_read_operation_request(self.GEO_GET_BIT, 141, 75)
        values = self._map_digital_values(di2.get('raw_data', []))
        self._translate_values(141, values, self.digitals, [
            (0, 1), (65, 66), (72, 75)
        ])

        di3 = await self.api.make_read_operation_request(self.GEO_GET_BIT, 262, 6)
        values = self._map_digital_values(di3.get('raw_data', []))
        self._translate_values(262, values, self.digitals, [
            (0, 1), (4, 6),
        ])

        return self.digitals

    @staticmethod
    def _map_integer_values(input_values: List[str]) -> List[int]:
        temp_values = [int(x, 16) for x in input_values]
        return [
            x - 65536 if x > 32768 else x for x in temp_values
        ]

    async def read_translate_integers(self) -> List[int]:
        en1 = await self.api.make_read_operation_request(self.GEO_GET_NUM, 5026, 38)
        values = self._map_integer_values(en1.get('raw_data', []))
        self._translate_values(5026 - 5001, values, self.integers, [
            (0, 1), (7, 8), (35, 38),
        ])

        en2 = await self.api.make_read_operation_request(self.GEO_GET_NUM, 5085, 17)
        values = self._map_integer_values(en2.get('raw_data', []))
        self._translate_values(5085 - 5001, values, self.integers, [
            (0, 4), (12, 17)
        ])

        en3 = await self.api.make_read_operation_request(self.GEO_GET_NUM, 5129, 35)
        values = self._map_integer_values(en3.get('raw_data', []))
        self._translate_values(5129 - 5001, values, self.integers, [
            (0, 1), (3, 20), (30, 35)
        ])

        return self.integers

    @staticmethod
    def _map_analogue_values(input_values: List[str]) -> List[float]:
        return [x / 10.0 for x in EcoGeo25100._map_integer_values(input_values)]

    async def read_translate_analogues(self):
        an1 = await self.api.make_read_operation_request(self.GEO_GET_NUM, 1, 38)
        values = self._map_analogue_values(an1.get('raw_data', []))
        self._translate_values(1, values, self.analogues, [
            (0, 6), (10, 24), (30, 34), (37, 38),
        ])

        an2 = await self.api.make_read_operation_request(self.GEO_GET_NUM, 41, 27)
        values = self._map_analogue_values(an2.get('raw_data', []))
        self._translate_values(41, values, self.analogues, [
            (0, 4), (25, 27)
        ])

        an3 = await self.api.make_read_operation_request(self.GEO_GET_NUM, 117, 39)
        values = self._map_analogue_values(an3.get('raw_data', []))
        self._translate_values(117, values, self.analogues, [
            (0, 22), (34, 39)
        ])

        an4 = await self.api.make_read_operation_request(self.GEO_GET_NUM, 161, 5)
        values = self._map_analogue_values(an4.get('raw_data', []))
        self._translate_values(161, values, self.analogues, [
            (0, 5)
        ])

        an5 = await self.api.make_read_operation_request(self.GEO_GET_NUM, 221, 7)
        values = self._map_analogue_values(an5.get('raw_data', []))
        self._translate_values(221, values, self.analogues, [
            (0, 7)
        ])

        for k,v in ANALOGUE_READINGS_MAPPINGS.items():
            log_debug(f'{k} = {self.analogues[v]}')

        return self.analogues





