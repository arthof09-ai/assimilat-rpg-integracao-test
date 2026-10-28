"""Boundary tests: local-only HTTP wrapper, no Notion integration."""
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

from vlab_gateway.core import Gateway
from vlab_gateway.http_local import server_for_tests

MASTER=b'H'*32
OPER='test-operator-http-token-abcdefghijk12345'
ADMIN='test-controller-http-token-abcdefghijk12345'

class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.g=Gateway(Path(self.tmp.name)/'http.db',MASTER)
        self.g.bootstrap_principal('operator','CM-000006','OPERATOR',OPER,bootstrap_secret=MASTER)
        self.g.bootstrap_principal('controller','CM-000001','CONTROLLER',ADMIN,bootstrap_secret=MASTER)
        self.server=server_for_tests(self.g)
        self.url='http://127.0.0.1:'+str(self.server.server_address[1])
        self.t=threading.Thread(target=self.server.serve_forever,daemon=True)
        self.t.start()

    def tearDown(self):
        self.server.shutdown();self.t.join(timeout=2);self.server.server_close();self.tmp.cleanup()

    def get(self,path):
        with urllib.request.urlopen(self.url+path,timeout=3) as h:
            return h.status,json.loads(h.read())

    def post(self,path,data=None,auth=None):
        req=urllib.request.Request(self.url+path,data=json.dumps(data or {}).encode(),method='POST',
                                   headers={'Content-Type':'application/json',**({'Authorization':'Bearer '+auth} if auth else {})})
        try:
            with urllib.request.urlopen(req,timeout=3) as h:
                return h.status,json.loads(h.read())
        except urllib.error.HTTPError as ex:
            return ex.code,json.loads(ex.read())

    def test_health_has_no_notion_adapter(self):
        code,x=self.get('/health')
        self.assertEqual(code,200)
        self.assertEqual(x['notion_write_adapter'],'DISABLED')

    def test_no_public_binding(self):
        self.assertEqual(self.server.server_address[0],'127.0.0.1')

    def test_http_no_auth(self):
        code,x=self.post('/v1/instance/allocate',{'allocation_key':'A'})
        self.assertEqual(code,401)

    def test_http_role_separation(self):
        code,x=self.post('/v1/instance/allocate',{'allocation_key':'A'},ADMIN)
        self.assertEqual(code,401)

    def test_http_local_flow_and_replay(self):
        code,r=self.post('/v1/instance/allocate',{'allocation_key':'A'},OPER)
        self.assertEqual(code,200)
        claim=r['result'];self.assertEqual(claim['instance'],'CM-000006-I0001')
        code,r=self.post('/v1/domain/claim',{'claim':claim},OPER)
        self.assertEqual(code,200);epoch=r['result']['epoch']
        body={'claim':claim,'epoch':epoch,'op_id':'test-op','idempotency_key':'t1','resource':'sandbox/test','payload':{'v':1}}
        self.assertEqual(self.post('/v1/intent/prepare',body,OPER)[0],200)
        commit={'claim':claim,'epoch':epoch,'op_id':'test-op'}
        self.assertEqual(self.post('/v1/intent/commit-local',commit,OPER)[0],200)
        self.assertEqual(self.post('/v1/intent/commit-local',commit,OPER)[1]['result']['status'],'IDEMPOTENT_REPLAY')
        self.assertEqual(self.post('/v1/control/snapshot',{},ADMIN)[1]['result']['notion_enforcement'],'NOT_IMPLEMENTED')

    def test_http_no_official_resource_scope(self):
        claim=self.post('/v1/instance/allocate',{'allocation_key':'A'},OPER)[1]['result']
        epoch=self.post('/v1/domain/claim',{'claim':claim},OPER)[1]['result']['epoch']
        body={'claim':claim,'epoch':epoch,'op_id':'bad','idempotency_key':'bad','resource':'Party/ficha','payload':{}}
        code,result=self.post('/v1/intent/prepare',body,OPER)
        self.assertEqual(code,409);self.assertEqual(result['error'],'RESOURCE_SCOPE_DENIED')

    def test_parallel_http_allocations_only_one(self):
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results=list(pool.map(lambda i:self.post('/v1/instance/allocate',{'allocation_key':'alloc-'+str(i)},OPER),range(8)))
        self.assertEqual(sum(code==200 for code,res in results),1)
        self.assertEqual(sum(code==409 for code,res in results),7)

    def test_impersonation_header_ignored(self):
        req=urllib.request.Request(self.url+'/v1/instance/allocate',
             data=b'{"allocation_key":"H"}',method='POST',headers={'X-Principal':'controller'})
        try:
            urllib.request.urlopen(req,timeout=3)
        except urllib.error.HTTPError as ex:
            self.assertEqual(ex.code,401)
        else:
            self.fail('Unsigned X-Principal header must not authenticate')

    def test_http_unsupported_routes_rejected(self):
        self.assertEqual(self.post('/v1/notion/write',{},OPER)[0],404)

if __name__=='__main__':unittest.main()
