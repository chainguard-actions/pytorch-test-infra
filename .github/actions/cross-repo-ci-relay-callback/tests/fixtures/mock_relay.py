#!/usr/bin/env python3
"""Local stand-in for the GitHub OIDC token endpoint and the CRCR relay.

Usage: mock_relay.py PORT OUTDIR

GET  /health          -> 200 "ok"
GET  /token?...       -> {"value": "mock-oidc-token-123"} (requires the bearer
                         request token "mock-request-token"); the query string
                         is appended to OUTDIR/token-requests.log
POST /callback        -> records the request to OUTDIR/req-NNN.json and answers
                         {"status": "ok"} or, for a late report, one
                         "attached" result per report
POST /late-invalid    -> late report answered with "invalid" for every report
POST /fail            -> HTTP 500
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1])
OUTDIR = sys.argv[2]
os.makedirs(OUTDIR, exist_ok=True)
COUNTER = [0]


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        data = json.dumps(obj).encode() if not isinstance(obj, str) else obj.encode()
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
            with open(os.path.join(OUTDIR, "token-requests.log"), "a") as f:
                f.write(self.path + "\n")
            if self.headers.get("Authorization") != "Bearer mock-request-token":
                self._send(401, {"message": "bad request token"})
                return
            self._send(200, {"value": "mock-oidc-token-123"})
            return
        self._send(404, {"message": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode()
        COUNTER[0] += 1
        try:
            body = json.loads(raw)
        except Exception:
            body = raw
        record = {
            "path": self.path,
            "auth": self.headers.get("Authorization"),
            "content_type": self.headers.get("Content-Type"),
            "body": body,
        }
        with open(os.path.join(OUTDIR, "req-%03d.json" % COUNTER[0]), "w") as f:
            json.dump(record, f, indent=2)

        if self.path.startswith("/fail"):
            self._send(500, {"error": "boom"})
            return
        if isinstance(body, dict) and body.get("event_type") == "late-report":
            result = "invalid" if self.path.startswith("/late-invalid") else "attached"
            results = [
                {
                    "result": result,
                    "job_name": r.get("job_name"),
                    "delivery_id": r.get("delivery_id"),
                    "detail": "mock detail",
                }
                for r in body.get("reports", [])
            ]
            self._send(200, {"status": "ok", "results": results})
            return
        self._send(200, {"status": "ok"})

    def log_message(self, fmt, *args):
        sys.stderr.write("mock: " + (fmt % args) + "\n")


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
