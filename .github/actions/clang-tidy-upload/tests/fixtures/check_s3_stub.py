#!/usr/bin/env python3
"""Test stub for tools/clang-tidy-checks/check_s3.py.

Records each invocation (s3 key + local file) to a log file and optionally
fails when the s3 key matches CHECK_S3_FAIL_KEY (simulating "binary unchanged").
"""
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--s3-key", required=True)
parser.add_argument("--local-file", required=True)
args = parser.parse_args()

log_path = os.environ.get("CHECK_S3_LOG", "check_s3_calls.log")
with open(log_path, "a") as f:
    f.write(f"{args.s3_key} {args.local_file}\n")

if not os.path.isfile(args.local_file):
    print(f"local file {args.local_file} not found", file=sys.stderr)
    sys.exit(2)

fail_key = os.environ.get("CHECK_S3_FAIL_KEY", "")
if fail_key and args.s3_key == fail_key:
    print(f"binary for {args.s3_key} has not changed", file=sys.stderr)
    sys.exit(1)

print(f"OK: {args.s3_key} differs from {args.local_file}")
