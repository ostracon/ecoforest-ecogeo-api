import unittest
import httpx
import os
from dotenv import load_dotenv
from ecoforest.api import EcoforestApi, EcoGeo25100

load_dotenv()


class TestEcoGeoAPI(unittest.IsolatedAsyncioTestCase):
    async def test_connection(self):
        auth = httpx.BasicAuth(os.getenv('ECOGEO_USERNAME'), os.getenv('ECOGEO_PASSWORD'))
        efapi = EcoforestApi("http://192.168.1.209", auth)
        gshp = EcoGeo25100(efapi)
        print(await gshp.read_translate_analogues())


if __name__ == '__main__':
    unittest.main()
