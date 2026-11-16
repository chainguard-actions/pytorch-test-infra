#!/usr/bin/env python3
"""Mock OIDC token endpoint + Cross-Repo CI Relay callback server for tests.

Usage: mock_relay.py PORT OUT_DIR

GET  /health          -> 200 {"ok": true}
GET  /token?...       -> 200 {"value": "mock-oidc-token-123"} (records request)
POST <path with fail> -> 500 {"error": "mock failure"}
POST <other path>     -> 200; late-report bodies get one "attached" result per report
Each POST is written to OUT_DIR/req-N.json as {"path","auth","content_type","body"}.
"""
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1])
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/mock-relay"
os.makedirs(OUT, exist_ok=True)
LOCK = threading.Lock()
COUNTER = [0]


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
            return self._send(200, {"ok": True})
        if self.path.startswith("/token"):
            with open(os.path.join(OUT, "token-request.json"), "w") as f:
                json.dump(
                    {"path": self.path, "auth": self.headers.get("Authorization", "")},
                    f,
                )
            return self._send(200, {"value": "mock-oidc-token-123"})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode("utf-8", "replace")
        with LOCK:
            COUNTER[0] += 1
            idx = COUNTER[0]
        with open(os.path.join(OUT, f"req-{idx}.json"), "w") as f:
            json.dump(
                {
                    "path": self.path,
                    "auth": self.headers.get("Authorization", ""),
                    "content_type": self.headers.get("Content-Type", ""),
                    "body": raw,
                },
                f,
            )
        if "fail" in self.path:
            return self._send(500, {"error": "mock failure"})
        try:
            body = json.loads(raw)
        except ValueError:
            body = {}
        if isinstance(body, dict) and body.get("event_type") == "late-report":
            results = [
                {
                    "result": "attached",
                    "job_name": r.get("job_name"),
                    "delivery_id": r.get("delivery_id"),
                }
                for r in body.get("reports", [])
                if isinstance(r, dict)
            ]
            return self._send(200, {"status": "ok", "results": results})
        return self._send(200, {"status": "ok"})

    def log_message(self, *args):
        pass


ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
