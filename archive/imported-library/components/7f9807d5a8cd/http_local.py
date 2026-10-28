"""Loopback-only demo HTTP service. Notion adapter is deliberately NOT installed.

Do not publish this endpoint or use for actual RPG protected writes. If port is
forwarded beyond loopback, security assumptions are broken. Production requires
an authenticated TLS proxy, per-domain ACL enforcement, secrets vault, and a
last-mile Notion integration with exclusive write credentials.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .core import Gateway, Rejected

MAX_HTTP_BODY=110000


def make_handler(gate):
    class Handler(BaseHTTPRequestHandler):
        server_version='VLABLocalDemo/0.4'
        sys_version=''

        def _reply(self,code,data):
            body=json.dumps(data,separators=(',',':'),ensure_ascii=False).encode('utf-8')
            self.send_response(code)
            self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Content-Length',str(len(body)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('X-Demo-Scope','LOCAL_SQLITE_ONLY')
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            # No headers, bodies or bearer tokens are logged.
            return

        def do_GET(self):
            if self.path == '/health':
                return self._reply(200,{'status':'RUNNING_LOCAL_SIMULATION',
                                        'notion_write_adapter':'DISABLED',
                                        'live_writer':'NOT_GRANTED'})
            return self._reply(404,{'error':'ROUTE_NOT_FOUND'})

        def do_POST(self):
            routes={'/v1/instance/allocate','/v1/domain/claim','/v1/intent/prepare',
                    '/v1/intent/commit-local','/v1/intent/dispatch-sim',
                    '/v1/domain/revoke-local','/v1/control/recover-unknown',
                    '/v1/control/snapshot'}
            if self.path not in routes:
                return self._reply(404,{'error':'ROUTE_NOT_FOUND'})
            auth=self.headers.get('Authorization','')
            if not auth.startswith('Bearer '):
                return self._reply(401,{'error':'AUTH_REQUIRED'})
            bearer=auth[7:]
            try:
                size=int(self.headers.get('Content-Length','-1'))
                if size < 0 or size>MAX_HTTP_BODY:
                    return self._reply(413,{'error':'CONTENT_LENGTH_OUT_OF_RANGE'})
                req=json.loads(self.rfile.read(size).decode('utf-8'))
                if not isinstance(req,dict):
                    return self._reply(400,{'error':'JSON_OBJECT_REQUIRED'})
                if self.path=='/v1/instance/allocate':
                    result=gate.allocate(bearer,req['allocation_key'])
                elif self.path=='/v1/domain/claim':
                    result={'epoch':gate.claim_domain(bearer,req['claim'])}
                elif self.path=='/v1/intent/prepare':
                    result=gate.prepare(bearer,req['claim'],req['epoch'],req['op_id'],
                                        req['idempotency_key'],req['resource'],req['payload'],expected_revision=req.get('expected_revision'))
                elif self.path=='/v1/intent/commit-local':
                    result=gate.commit_local(bearer,req['claim'],req['epoch'],req['op_id'])
                elif self.path=='/v1/intent/dispatch-sim':
                    result=gate.begin_external_dispatch_simulation(bearer,req['claim'],req['epoch'],req['op_id'])
                elif self.path=='/v1/domain/revoke-local':
                    result=gate.revoke_and_fence(bearer)
                elif self.path=='/v1/control/recover-unknown':
                    result=gate.recover_uncertain(bearer)
                elif self.path=='/v1/control/snapshot':
                    result=gate.snapshot(bearer)
                self._reply(200,{'ok':True,'result':result,'enforcement':'LOCAL_SQLITE_ONLY'})
            except (KeyError,ValueError,TypeError,UnicodeDecodeError,json.JSONDecodeError):
                self._reply(400,{'error':'INVALID_REQUEST'})
            except Rejected as ex:
                code=401 if ex.code in ('UNAUTHENTICATED','ROLE_DENIED','IDENTITY_DENIED') else 409
                self._reply(code,{'error':ex.code,'notion_fencing':'NOT_ESTABLISHED'})
            except Exception:
                # Fail closed; no exception content or secrets to clients.
                self._reply(500,{'error':'SERVER_ERROR_FAIL_CLOSED'})
    return Handler


def server_for_tests(gate):
    return ThreadingHTTPServer(('127.0.0.1',0),make_handler(gate))


def main():
    host=os.getenv('VLAB_GATE_HOST','127.0.0.1')
    if host!='127.0.0.1':
        raise SystemExit('DENY: demo must bind 127.0.0.1; no remote production service')
    db=os.getenv('VLAB_GATE_DB','')
    if not db:
        raise SystemExit('DENY: VLAB_GATE_DB required')
    try:port=int(os.getenv('VLAB_GATE_PORT','8765'))
    except ValueError:raise SystemExit('DENY: invalid port')
    gate=Gateway.from_env(db)
    server=ThreadingHTTPServer((host,port),make_handler(gate))
    print('LOCAL-SIMULATION ONLY; NOTION-WRITER=OFF; '+str(server.server_address),flush=True)
    server.serve_forever()

if __name__=='__main__':main()
