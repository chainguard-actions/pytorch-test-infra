#!/usr/bin/env python3
"""Test stub for tools/clang-tidy-checks/check_s3.py.

Records the arguments it was invoked with to $CHECK_S3_LOG (one line per call)
and exits with $CHECK_S3_EXIT (default 0). Avoids any real S3 access.
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
    f.write(f"{args.s3_key} {args.local_file} exists={os.path.exists(args.local_file)}\n")

sys.exit(int(os.environ.get("CHECK_S3_EXIT", "0")))
