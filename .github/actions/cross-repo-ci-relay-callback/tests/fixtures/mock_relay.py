#!/usr/bin/env python3
"""Local mock for the GitHub OIDC token endpoint and the CRCR relay callback.

act does not provide an OIDC token service, so tests point
ACTIONS_ID_TOKEN_REQUEST_URL at this server. The callback-url input is also
pointed here so the POSTed payload can be recorded and asserted on.

Every request is appended (as one JSON line) to $MOCK_LOG.

POST path behaviour:
  .../fail  -> HTTP 500
  .../late  -> HTTP 200 with an "attached" result per report
  otherwise -> HTTP 200 {"status": "ok"}
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

LOG = os.environ.get("MOCK_LOG", "/tmp/mock-relay/requests.jsonl")
PORT = int(os.environ.get("MOCK_PORT", "8765"))
TOKEN = "mock-oidc-token-12345"


class Handler(BaseHTTPRequestHandler):
    def _record(self, method, body):
        with open(LOG, "a") as f:
            f.write(
                json.dumps(
                    {
                        "method": method,
                        "path": self.path,
                        "authorization": self.headers.get("Authorization", ""),
                        "body": body,
                    }
                )
                + "\n"
            )

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
        self._record("GET", "")
        self._send(200, {"value": TOKEN})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length).decode("utf-8", "replace")
        self._record("POST", body)
        if "/fail" in self.path:
            return self._send(500, {"error": "mock failure"})
        if "/late" in self.path:
            try:
                reports = json.loads(body).get("reports", [])
            except Exception:
                reports = []
            return self._send(
                200,
                {
                    "status": "ok",
                    "results": [
                        {
                            "result": "attached",
                            "job_name": r.get("job_name"),
                            "delivery_id": r.get("delivery_id"),
                        }
                        for r in reports
                    ],
                },
            )
        self._send(200, {"status": "ok"})

    def log_message(self, fmt, *args):
        sys.stderr.write("mock-relay: " + (fmt % args) + "\n")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
