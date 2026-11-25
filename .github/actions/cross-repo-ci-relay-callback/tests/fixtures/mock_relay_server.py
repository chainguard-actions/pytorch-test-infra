#!/usr/bin/env python3
"""Local stand-in for the GitHub OIDC token endpoint and the CRCR relay.

Usage: mock_relay_server.py PORT CAPTURE_DIR

  GET  /health          -> 200 "ok"
  GET  /token?...       -> 200 {"value": "fake-oidc-jwt"}  (OIDC token endpoint)
  POST /fail            -> 500 {"error": "boom"}            (captured)
  POST anything else    -> 200, captured to CAPTURE_DIR/<n>.json
       late-report bodies get one result per report: "invalid" for a report
       whose job_name is "make-invalid", "attached" otherwise.
"""

import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1])
CAPTURE_DIR = sys.argv[2]
os.makedirs(CAPTURE_DIR, exist_ok=True)
_lock = threading.Lock()
_counter = [0]


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
        elif self.path.startswith("/token"):
            self._send(200, {"value": "fake-oidc-jwt"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode()
        try:
            body = json.loads(raw)
        except json.JSONDecodeError:
            body = raw
        with _lock:
            _counter[0] += 1
            n = _counter[0]
        with open(os.path.join(CAPTURE_DIR, f"{n:03d}.json"), "w") as f:
            json.dump(
                {
                    "path": self.path,
                    "auth": self.headers.get("Authorization", ""),
                    "content_type": self.headers.get("Content-Type", ""),
                    "body": body,
                },
                f,
            )
        if self.path.startswith("/fail"):
            self._send(500, {"error": "boom"})
            return
        if isinstance(body, dict) and body.get("event_type") == "late-report":
            results = []
            for r in body.get("reports", []):
                job = r.get("job_name")
                result = "invalid" if job == "make-invalid" else "attached"
                entry = {
                    "result": result,
                    "job_name": job,
                    "delivery_id": r.get("delivery_id"),
                }
                if result == "invalid":
                    entry["detail"] = "rejected by mock"
                results.append(entry)
            self._send(200, {"status": "ok", "results": results})
            return
        self._send(200, {"status": "ok"})

    def log_message(self, fmt, *args):
        sys.stderr.write("mock: " + (fmt % args) + "\n")


ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
