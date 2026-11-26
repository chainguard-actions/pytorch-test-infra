#!/usr/bin/env python3
"""Local mock for the GitHub OIDC token endpoint and the CRCR relay server.

- GET  /token...  -> {"value": "fake-oidc-token-for-test"} (what core.getIDToken expects)
- GET  /health    -> {"ok": true}
- POST /...       -> records the request to <dir>/request-N.json and answers
                     according to --status / --late-result.

Binds an ephemeral port on 127.0.0.1 and writes it to <dir>/port.
"""
import argparse
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

parser = argparse.ArgumentParser()
parser.add_argument("--dir", default="/tmp/mock-relay")
parser.add_argument("--status", type=int, default=200)
parser.add_argument("--late-result", default="attached")
args = parser.parse_args()

os.makedirs(args.dir, exist_ok=True)
lock = threading.Lock()
counter = [0]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *a):
        sys.stderr.write((fmt % a) + "\n")
        sys.stderr.flush()

    def _send(self, code, obj):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/token"):
            with lock:
                with open(os.path.join(args.dir, "token-requests.log"), "a") as f:
                    f.write(
                        json.dumps(
                            {
                                "path": self.path,
                                "authorization": self.headers.get("Authorization", ""),
                            }
                        )
                        + "\n"
                    )
            self._send(200, {"value": "fake-oidc-token-for-test"})
        elif self.path == "/health":
            self._send(200, {"ok": True})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode("utf-8", "replace")
        try:
            body = json.loads(raw)
        except ValueError:
            body = raw
        with lock:
            counter[0] += 1
            n = counter[0]
            with open(os.path.join(args.dir, "request-%d.json" % n), "w") as f:
                json.dump(
                    {
                        "path": self.path,
                        "headers": {k.lower(): v for k, v in self.headers.items()},
                        "body": body,
                    },
                    f,
                    indent=2,
                )
        if args.status != 200:
            self._send(args.status, {"error": "mock failure"})
            return
        if isinstance(body, dict) and body.get("event_type") == "late-report":
            results = [
                {
                    "result": args.late_result,
                    "job_name": r.get("job_name"),
                    "delivery_id": r.get("delivery_id"),
                    "detail": "mock detail",
                }
                for r in body.get("reports", [])
                if isinstance(r, dict)
            ]
            self._send(200, {"status": "ok", "results": results})
            return
        self._send(200, {"status": "ok"})


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
port = server.server_address[1]
with open(os.path.join(args.dir, "port.tmp"), "w") as f:
    f.write(str(port))
os.rename(os.path.join(args.dir, "port.tmp"), os.path.join(args.dir, "port"))
server.serve_forever()
