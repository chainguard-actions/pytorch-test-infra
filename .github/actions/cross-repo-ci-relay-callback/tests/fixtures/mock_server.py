#!/usr/bin/env python3
"""Local mock for the OIDC token endpoint (GET) and the relay callback (POST).

Usage: mock_server.py PORT OUT_DIR [POST_STATUS] [POST_BODY]

GET  any path  -> {"value": "fake-oidc-token"}
POST any path  -> records body to OUT_DIR/request-N.json and the Authorization
                  header to OUT_DIR/auth-N.txt; replies POST_STATUS / POST_BODY.
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1])
OUT_DIR = sys.argv[2]
POST_STATUS = int(sys.argv[3]) if len(sys.argv) > 3 else 200
POST_BODY = sys.argv[4] if len(sys.argv) > 4 else '{"status": "ok"}'

os.makedirs(OUT_DIR, exist_ok=True)
COUNTER = {"n": 0}


class Handler(BaseHTTPRequestHandler):
    def _reply(self, code, body):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        with open(os.path.join(OUT_DIR, "oidc-requests.log"), "a") as f:
            f.write(self.path + "\n")
        if self.path.startswith("/ready"):
            self._reply(200, '{"ready": true}')
            return
        self._reply(200, json.dumps({"value": "fake-oidc-token"}))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode()
        COUNTER["n"] += 1
        n = COUNTER["n"]
        with open(os.path.join(OUT_DIR, f"request-{n}.json"), "w") as f:
            f.write(body)
        with open(os.path.join(OUT_DIR, f"auth-{n}.txt"), "w") as f:
            f.write(self.headers.get("Authorization", ""))
        self._reply(POST_STATUS, POST_BODY)

    def log_message(self, fmt, *args):
        sys.stderr.write("mock: " + (fmt % args) + "\n")


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
