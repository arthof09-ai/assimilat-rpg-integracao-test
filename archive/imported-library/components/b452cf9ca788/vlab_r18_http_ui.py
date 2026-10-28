"""Loopback-only browser frontend for the existing R17 VLAB motor.

Usage: python fusion_stage12/vlab_r18_http_ui.py
Dependencies: Python standard library, recovered R17 tree. NO Notion endpoints.
"""
from __future__ import annotations

from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json
import sys
import time
import webbrowser

from vlab_r18_interactive_core import BattleService, BattleHold, canonical

HERE = Path(__file__).resolve().parent
ASSETS = {
    "/": ("text/html; charset=utf-8", HERE / "vlab_r18_ui.html"),
    "/vlab.css": ("text/css; charset=utf-8", HERE / "vlab_r18_ui.css"),
    "/vlab.js": ("text/javascript; charset=utf-8", HERE / "vlab_r18_ui.js"),
}


class Handler(BaseHTTPRequestHandler):
    server_version = "VLAB-R18-TEST-ONLY"

    def log_message(self, fmt, *args):
        sys.stderr.write("[VLAB LOCAL] " + fmt % args + "\n")

    def _reply(self, status, content, mime="application/json; charset=utf-8", extra=None):
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'self'; connect-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'")
        self.send_header("Referrer-Policy", "no-referrer")
        if extra:
            for key, value in extra.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(content)

    def _host_allowed(self):
        host = self.headers.get("Host", "").split(":")[0].lower()
        return host in ("127.0.0.1", "localhost")

    def _reject(self, reason, status=400):
        self._reply(status, canonical({"status":"HOLD","error":reason,
                           "official_writes":0,"automatic_retry":False}))

    def do_GET(self):
        if not self._host_allowed():
            return self._reject("ONLY_LOCALHOST_HOST_ACCEPTED", 403)
        path = urlsplit(self.path).path
        if path in ASSETS:
            mime, filepath = ASSETS[path]
            if not filepath.is_file():
                return self._reject("STATIC_FILE_UNAVAILABLE",404)
            return self._reply(200, filepath.read_bytes(), mime)
        try:
            if path == "/api/state":
                return self._reply(200, canonical(self.server.battle.view()))
            if path == "/api/receipt":
                data = self.server.battle.receipt()
                filename = "VLAB-R18-" + data["session"]["session_id"] + "-RECIBO.json"
                return self._reply(200, json.dumps(data, indent=2, ensure_ascii=False).encode(),
                   extra={"Content-Disposition": f'attachment; filename="{filename}"'})
        except Exception as error:
            return self._reject("READBACK_HOLD:" + str(error),409)
        self._reject("ROUTE_NOT_FOUND",404)

    def do_POST(self):
        if not self._host_allowed():
            return self._reject("ONLY_LOCALHOST_HOST_ACCEPTED",403)
        if self.headers.get("X-VLAB-UI") != "1":
            return self._reject("EXPLICIT_LOCAL_UI_HEADER_REQUIRED",403)
        if not self.headers.get("Content-Type","").startswith("application/json"):
            return self._reject("JSON_CONTENT_TYPE_REQUIRED",415)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 2 or length > 4096:
                return self._reject("BAD_REQUEST_SIZE",413)
            raw = self.rfile.read(length)
            data = json.loads(raw)
            if not isinstance(data,dict):
                return self._reject("OBJECT_BODY_REQUIRED")
        except (ValueError,UnicodeDecodeError):
            return self._reject("INVALID_REQUEST_JSON")
        path = urlsplit(self.path).path
        try:
            if path == "/api/new":
                if set(data) != {"scenario"}:
                    raise BattleHold("EXACT_NEW_SCENARIO_FIELDS_REQUIRED")
                out = self.server.battle.new(data["scenario"])
            elif path == "/api/act":
                out = self.server.battle.act(data)
            elif path == "/api/undo":
                if set(data) != {"request_id"}:
                    raise BattleHold("EXACT_UNDO_FIELDS_REQUIRED")
                out = self.server.battle.undo(data["request_id"])
            elif path == "/api/recover":
                if data:
                    raise BattleHold("RECOVER_EMPTY_OBJECT_REQUIRED")
                out = self.server.battle.recover()
            else:
                return self._reject("ROUTE_NOT_FOUND",404)
            return self._reply(200, canonical(out))
        except (BattleHold,ValueError,KeyError,TypeError) as error:
            return self._reject(str(error),409)
        except Exception as error:
            # No automatic retries, no hidden call to any official service.
            return self._reject("EXPERIMENT_HOLD_REOPEN_BEFORE_RETRY:"+str(error),500)


def main(argv=None):
    p=ArgumentParser(description="VLAB — interface humana de combate experimental (NÃO OFICIAL)")
    p.add_argument("--port", type=int, default=0, help="porta local; 0 escolhe uma livre")
    p.add_argument("--data-dir", default=str(Path.home() / "VLAB-R18-Experimentos"))
    p.add_argument("--no-browser", action="store_true")
    a=p.parse_args(argv)
    if a.port < 0 or a.port > 65535:
        p.error("porta inválida")
    try:
        battle=BattleService(a.data_dir)
    except Exception as e:
        print("VLAB HOLD: não foi possível carregar dados locais. Nenhum reset automático.",file=sys.stderr)
        print(str(e),file=sys.stderr)
        return 2
    srv=ThreadingHTTPServer(("127.0.0.1", a.port),Handler)
    srv.battle=battle
    url=f"http://127.0.0.1:{srv.server_address[1]}/"
    print("VLAB R18 / EXPERIMENTAL SOMENTE / SEM NOTION",flush=True)
    print("ABRIR NO NAVEGADOR: " + url,flush=True)
    print("DADOS LOCAIS: " + str(battle.dir),flush=True)
    print("ENCERRAR SERVIDOR: Ctrl+C",flush=True)
    if not a.no_browser:
        webbrowser.open_new_tab(url)
    try:
        srv.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
    return 0

if __name__=="__main__":
    sys.exit(main())
