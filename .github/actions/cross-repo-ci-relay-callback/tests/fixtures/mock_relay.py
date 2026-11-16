#!/usr/bin/env python3
"""Local mock for the OIDC ID-token endpoint and the CRCR relay callback.

Usage: mock_relay.py <port> <out_dir>

GET  /health        -> 200
GET  /token?...     -> 200 {"value": "fake-oidc-token"}  (core.getIDToken)
POST /fail...       -> 500 {"error": "mock relay failure"} (body recorded)
POST anything else  -> 200 {"ok": true}                 (body recorded)

Each POST is recorded as <out_dir>/request-<n>.json (raw body) and
<out_dir>/request-<n>.meta.json (path + headers).
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1])
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/health"):
            self._send(200, {"ok": True})
        elif self.path.startswith("/token"):
            with open(os.path.join(OUT, "token-requests.log"), "a") as f:
                f.write(self.path + "\t" + self.headers.get("Authorization", "") + "\n")
            self._send(200, {"value": "fake-oidc-token"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        body = self.rfile.read(length)
        n = len([p for p in os.listdir(OUT) if p.startswith("request-") and p.endswith(".meta.json")])
        with open(os.path.join(OUT, f"request-{n}.json"), "wb") as f:
            f.write(body)
        with open(os.path.join(OUT, f"request-{n}.meta.json"), "w") as f:
            json.dump(
                {
                    "path": self.path,
                    "authorization": self.headers.get("Authorization", ""),
                    "content_type": self.headers.get("Content-Type", ""),
                },
                f,
            )
        if self.path.startswith("/fail"):
            self._send(500, {"error": "mock relay failure"})
        else:
            self._send(200, {"ok": True})

    def log_message(self, fmt, *args):
        sys.stderr.write("mock_relay: " + (fmt % args) + "\n")


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
