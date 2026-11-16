#!/usr/bin/env python3
"""Mock of tools/clang-tidy-checks/check_s3.py used by tests.

Records its arguments to /tmp/check_s3_calls.log and verifies the local file
exists. Exits 1 if /tmp/check_s3_fail exists (to simulate a failed check).
"""
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--s3-key", required=True)
parser.add_argument("--local-file", required=True)
args = parser.parse_args()

with open("/tmp/check_s3_calls.log", "a") as f:
    f.write(f"{args.s3_key} {args.local_file}\n")

if os.path.exists("/tmp/check_s3_fail"):
    print(f"mock check_s3: simulated failure for {args.s3_key}")
    sys.exit(1)

if not os.path.isfile(args.local_file):
    print(f"mock check_s3: local file {args.local_file} not found")
    sys.exit(2)

print(f"mock check_s3: ok {args.s3_key} {args.local_file}")
