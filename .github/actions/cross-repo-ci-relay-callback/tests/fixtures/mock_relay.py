#!/usr/bin/env python3
"""Local stand-in for the OIDC token endpoint and the CRCR relay callback.

Usage: mock_relay.py PORT RECORD_DIR

GET  /health          -> 200 "ok"
GET  /token?...       -> {"value": "mock-oidc-token-123"} (OIDC token endpoint)
POST /fail...         -> 500 {"error": "boom"}
POST anything else    -> recorded to RECORD_DIR/requests.jsonl, then 200.
                         Late reports get a per-report "attached" result.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1])
RECORD_DIR = sys.argv[2]
os.makedirs(RECORD_DIR, exist_ok=True)
TOKEN = "mock-oidc-token-123"


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/health"):
            self._send(200, "ok")
            return
        if self.path.startswith("/token"):
            with open(os.path.join(RECORD_DIR, "token_requests.jsonl"), "a") as f:
                f.write(json.dumps({
                    "path": self.path,
                    "auth": self.headers.get("Authorization", ""),
                }) + "\n")
            self._send(200, json.dumps({"value": TOKEN}))
            return
        self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode()
        try:
            body = json.loads(raw)
        except Exception:
            body = raw
        with open(os.path.join(RECORD_DIR, "requests.jsonl"), "a") as f:
            f.write(json.dumps({
                "path": self.path,
                "auth": self.headers.get("Authorization", ""),
                "content_type": self.headers.get("Content-Type", ""),
                "body": body,
            }) + "\n")
        if self.path.startswith("/fail"):
            self._send(500, json.dumps({"error": "boom"}))
            return
        if isinstance(body, dict) and body.get("event_type") == "late-report":
            results = [
                {
                    "result": "attached",
                    "job_name": r.get("job_name"),
                    "delivery_id": r.get("delivery_id"),
                }
                for r in body.get("reports", [])
            ]
            self._send(200, json.dumps({"status": "ok", "results": results}))
            return
        self._send(200, json.dumps({"status": "ok"}))

    def log_message(self, fmt, *args):
        sys.stderr.write("mock_relay: " + (fmt % args) + "\n")


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
