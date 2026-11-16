#!/usr/bin/env python3
"""Test stub for tools/clang-tidy-checks/check_s3.py.

Records its arguments to /tmp/check_s3_calls.log (one line per call) and
exits 1 if /tmp/check_s3_fail exists, otherwise 0.
"""
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--s3-key", required=True)
parser.add_argument("--local-file", required=True)
args = parser.parse_args()

with open("/tmp/check_s3_calls.log", "a") as f:
    f.write(f"s3-key={args.s3_key} local-file={args.local_file}\n")

if os.path.exists("/tmp/check_s3_fail"):
    print("stub: simulated check failure")
    sys.exit(1)
print("stub: check ok")
sys.exit(0)
