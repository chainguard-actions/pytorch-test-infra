#!/usr/bin/env python3
"""Minimal local stand-in for the CRCR relay callback endpoint.

Records every POST body (and the Authorization header) under OUT_DIR and
answers 200 with a JSON body. For late reports it answers one "attached"
result per report so the action's summary logic is satisfied.
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18080
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else "/tmp/crcr-requests"
os.makedirs(OUT_DIR, exist_ok=True)
COUNTER = {"n": 0}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("mock-relay: " + (fmt % args) + "\n")

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length).decode("utf-8", "replace")
        COUNTER["n"] += 1
        n = COUNTER["n"]
        with open(os.path.join(OUT_DIR, f"{n}.json"), "w") as f:
            f.write(body)
        with open(os.path.join(OUT_DIR, f"{n}.auth"), "w") as f:
            f.write(self.headers.get("Authorization", ""))
        resp = {"status": "ok"}
        try:
            data = json.loads(body)
        except Exception:
            data = {}
        if isinstance(data, dict) and data.get("event_type") == "late-report":
            resp["results"] = [
                {
                    "result": "attached",
                    "job_name": r.get("job_name"),
                    "delivery_id": r.get("delivery_id"),
                }
                for r in data.get("reports", [])
                if isinstance(r, dict)
            ]
        out = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
