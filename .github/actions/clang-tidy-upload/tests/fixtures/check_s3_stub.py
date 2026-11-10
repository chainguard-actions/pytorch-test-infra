#!/usr/bin/env python3
"""Test stub for tools/clang-tidy-checks/check_s3.py.

Records its arguments to $CHECK_S3_LOG and verifies the local file exists.
Exits non-zero when STUB_FAIL=1 to simulate a sanity-check failure.
"""
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--s3-key", required=True)
parser.add_argument("--local-file", required=True)
args = parser.parse_args()

log = os.environ.get("CHECK_S3_LOG", "/tmp/check_s3.log")
with open(log, "a") as f:
    f.write(f"{args.s3_key} {args.local_file}\n")

if not os.path.isfile(args.local_file):
    print(f"local file {args.local_file} missing", file=sys.stderr)
    sys.exit(2)

if os.environ.get("STUB_FAIL") == "1":
    print("simulated: binary has changed", file=sys.stderr)
    sys.exit(1)

print(f"OK: {args.s3_key} matches {args.local_file}")
