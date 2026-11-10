#!/usr/bin/env python3
"""Stub for tools/clang-tidy-checks/check_s3.py used by act tests.

Records each invocation's arguments to $CHECK_S3_LOG (default: check_s3.log in
the current directory) and exits with $CHECK_S3_EXIT (default 0).
"""
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--s3-key", required=True)
parser.add_argument("--local-file", required=True)
args = parser.parse_args()

log = os.environ.get("CHECK_S3_LOG", "check_s3.log")
with open(log, "a") as f:
    f.write(f"{args.s3_key} {args.local_file} exists={os.path.isfile(args.local_file)}\n")

sys.exit(int(os.environ.get("CHECK_S3_EXIT", "0")))
