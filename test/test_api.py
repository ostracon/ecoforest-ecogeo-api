import unittest
import httpx
import os
from dotenv import load_dotenv
from ecoforest.api import EcoforestApi, EcoGeo25100

load_dotenv()

"""
Some data for mocking later

DEBUG:ecoforest.api:error_geo_get_reg=0
dir=221&num=7&002C&0000&FFFB&0005&0000&0000&0000
0
DEBUG:ecoforest.api:reply = {'error_geo_get_reg': '0', 'dir': '221', 'num': '7', 'raw_data': ['002C', '0000', 'FFFB', '0005', '0000', '0000', '0000'], 'error_check': '0'}
DEBUG:ecoforest.api:Received from POST with data {'error_geo_get_reg': '0', 'dir': '221', 'num': '7', 'raw_data': ['002C', '0000', 'FFFB', '0005', '0000', '0000', '0000'], 'error_check': '0'}
[0.0, 6.3, 6.7, 2.1, 46.1, 43.8, 2.2, 0.0, 0.0, 0.0, 0.0, 51.9, 22.0, 46.3, 46.3, 46.3, 46.3, 46.3, -999.9, 0.2, 4.0, 46.3, -999.9, 46.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 99.9, 99.9, 99.9, 99.9, 0.0, 0.0, 0.0, 52.0, 0.0, 0.0, 3.0, 50.0, 3.0, 21.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 23.0, 28.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 2.0, 20.0, 2.0, 21.5, 13.5, 46.3, 40.0, 40.0, 40.0, 40.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.4, 0.0, -0.5, 0.5, 0.0, 0.0, 0.0]
"""

class TestEcoGeoAPI(unittest.IsolatedAsyncioTestCase):
    async def test_connection(self):
        auth = httpx.BasicAuth(os.getenv('ECOGEO_USERNAME'), os.getenv('ECOGEO_PASSWORD'))
        efapi = EcoforestApi("http://192.168.1.209", auth)
        gshp = EcoGeo25100(efapi)
        print(await gshp.read_translate_analogues())


if __name__ == '__main__':
    unittest.main()
