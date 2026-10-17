# Ecoforest HP HTTP reader

Read-only local client for ecoGEO HP 25–100. See [register coverage and safety](READ_ONLY_REGISTERS.md).

```python
import asyncio
import os
import httpx
from ecoforest.api import EcoforestApi, EcoGeo25100

async def main():
    async with httpx.AsyncClient(base_url=os.environ["ECOGEO_URL"]) as client:
        api = EcoforestApi(os.environ["ECOGEO_URL"], client=client,
                           auth=httpx.BasicAuth(os.environ["ECOGEO_USERNAME"],
                                                os.environ["ECOGEO_PASSWORD"]))
        hp = EcoGeo25100(api)
        values = await hp.read_all()
        print(values)
        print("Unsupported/failed optional reads:", hp.failed_reads)

asyncio.run(main())
```

`read_all()` returns all 360 named HP fields; `mapping` and `raw_values` retain
source metadata and the underlying payload. Legacy `read_translate_*` methods
remain available but expose only their original subset. Do not run concurrent
pollers or poll faster than the existing HA 60-second interval.

Offline tests: `python -m unittest discover -s test -v`.
The older live test requires an explicit `ECOFOREST_LIVE_TEST=1` opt-in and
python-dotenv; normal test discovery does not read credentials or contact a pump.
