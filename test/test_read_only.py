import unittest
from unittest.mock import AsyncMock, patch
from urllib.parse import parse_qs
import httpx
from ecoforest.api import EcoforestApi, EcoGeo25100
from ecoforest.exceptions import EcoforestConnectionError

class ReadOnlyApiTests(unittest.IsolatedAsyncioTestCase):
    async def test_complete_read_and_write_block(self):
        requests=[]
        def respond(req):
            d={k:int(v[0]) for k,v in parse_qs(req.content.decode()).items()}; requests.append(d)
            op,a,n=d['idOperacion'],d['dir'],d['num']; header='bit' if op==2001 else 'reg'
            vals=['0' if op==2001 else '0000']*n
            return httpx.Response(200,text=f'error_geo_get_{header}=0\ndir={a}&num={n}&'+'&'.join(vals)+'\n0')
        async with httpx.AsyncClient(base_url='http://example.invalid',transport=httpx.MockTransport(respond)) as c:
            api=EcoforestApi('http://example.invalid',client=c)
            for op in [2011,2012]:
                with self.assertRaises(ValueError): await api.make_read_operation_request(op,1,1)
            self.assertEqual(requests,[])
            device=EcoGeo25100(api)
            with patch('ecoforest.api.asyncio.sleep',new=AsyncMock()):values=await device.read_all()
            self.assertEqual(len(values),570)
            self.assertEqual(device.failed_reads,[])
            self.assertTrue(all(q['idOperacion'] in [2001,2002] for q in requests))
    async def test_required_read_retries_twice_then_recovers(self):
        attempts=0
        def respond(req):
            nonlocal attempts
            d={k:int(v[0]) for k,v in parse_qs(req.content.decode()).items()}
            op,a,n=d['idOperacion'],d['dir'],d['num']; header='bit' if op==2001 else 'reg'
            if op==2001 and a==1 and attempts<2:
                attempts+=1
                return httpx.Response(200,text='error_geo_get_bit=-1')
            vals=['0' if op==2001 else '0000']*n
            return httpx.Response(200,text=f'error_geo_get_{header}=0\ndir={a}&num={n}&'+'&'.join(vals)+'\n0')
        async with httpx.AsyncClient(base_url='http://example.invalid',transport=httpx.MockTransport(respond)) as c:
            device=EcoGeo25100(EcoforestApi('http://example.invalid',client=c))
            with patch('ecoforest.api.asyncio.sleep',new=AsyncMock()):
                values=await device.read_all()
            self.assertEqual(attempts,2)
            self.assertEqual(len(values),570)

    async def test_connection_failure_is_not_attribute_error(self):
        def fail(req):raise httpx.ConnectError('offline',request=req)
        async with httpx.AsyncClient(base_url='http://example.invalid',transport=httpx.MockTransport(fail)) as c:
            api=EcoforestApi('http://example.invalid',client=c)
            with self.assertRaises(EcoforestConnectionError):await api.make_read_operation_request(2002,1,1)
