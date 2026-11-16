#!/usr/bin/env python3
"""Mock OIDC token endpoint + Cross-Repo CI Relay callback endpoint.

Usage: mock_relay_server.py PORT OUTDIR

GET  /health        -> 200 {"ok": true}
GET  /token?...     -> 200 {"value": "fake-oidc-token-for-test"}  (logged to OUTDIR/token-requests.log)
POST /fail...       -> 500 (request recorded)
POST anything else  -> 200; late-report bodies get one "attached" result per report.
Every POST is recorded to OUTDIR/req-N.json as {"path", "auth", "content_type", "body"}.
"""
import itertools
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1])
OUTDIR = sys.argv[2]
os.makedirs(OUTDIR, exist_ok=True)
COUNTER = itertools.count(1)


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
            with open(os.path.join(OUTDIR, "token-requests.log"), "a") as f:
                f.write(self.path + "\n")
            return self._send(200, {"value": "fake-oidc-token-for-test"})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8", "replace")
        idx = next(COUNTER)
        record = {
            "path": self.path,
            "auth": self.headers.get("Authorization"),
            "content_type": self.headers.get("Content-Type"),
            "body": raw,
        }
        with open(os.path.join(OUTDIR, "req-%d.json" % idx), "w") as f:
            json.dump(record, f)
        if self.path.startswith("/fail"):
            return self._send(500, {"error": "mock relay failure"})
        try:
            body = json.loads(raw)
        except json.JSONDecodeError:
            body = {}
        if isinstance(body, dict) and body.get("event_type") == "late-report":
            results = [
                {
                    "result": "attached",
                    "job_name": r.get("job_name"),
                    "delivery_id": r.get("delivery_id"),
                }
                for r in body.get("reports", [])
            ]
            return self._send(200, {"status": "ok", "results": results})
        return self._send(200, {"status": "ok"})

    def log_message(self, fmt, *args):
        sys.stderr.write("mock: " + (fmt % args) + "\n")


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
