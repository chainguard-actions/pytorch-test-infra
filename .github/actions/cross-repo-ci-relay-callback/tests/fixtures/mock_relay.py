#!/usr/bin/env python3
"""Tiny local stand-in for the OIDC token endpoint and the CRCR relay.

Usage: mock_relay.py PORT OUTDIR

GET  /token   -> {"value": "mock-oidc-token"}   (actions/core getIDToken)
GET  /health  -> {"ok": true}
POST /...     -> records body to OUTDIR/reqN.json and metadata to
                 OUTDIR/reqN.meta; returns 500 if the path ends in /fail,
                 otherwise 200.
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1])
OUTDIR = sys.argv[2]
os.makedirs(OUTDIR, exist_ok=True)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/token":
            self._send(200, {"value": "mock-oidc-token"})
        elif path == "/health":
            self._send(200, {"ok": True})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length)
        path = self.path.split("?")[0].rstrip("/")
        idx = len([f for f in os.listdir(OUTDIR) if f.endswith(".json")])
        with open(os.path.join(OUTDIR, f"req{idx}.json"), "wb") as f:
            f.write(body)
        with open(os.path.join(OUTDIR, f"req{idx}.meta"), "w") as f:
            json.dump(
                {
                    "path": path,
                    "auth": self.headers.get("Authorization", ""),
                    "content_type": self.headers.get("Content-Type", ""),
                },
                f,
            )
        if path.endswith("/fail"):
            self._send(500, {"error": "mock failure"})
        else:
            self._send(200, {"ok": True})

    def log_message(self, fmt, *args):
        sys.stderr.write("mock_relay: " + (fmt % args) + "\n")


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
