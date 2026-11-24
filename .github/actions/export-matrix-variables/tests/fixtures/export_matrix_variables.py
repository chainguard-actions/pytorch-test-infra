#!/usr/bin/env python3
"""Stub of test-infra/.github/scripts/export_matrix_variables.py used by tests.

Records its arguments to $RUNNER_TEMP/stub_args.txt and prints KEY=VALUE
lines for each entry in the input JSON (quoted when requested).
"""
import json
import os
import sys

args = sys.argv[1:]
quotes = "--add-quotes-around-value" in args
input_file = args[args.index("--input-file") + 1]
with open(input_file) as fh:
    data = json.load(fh)

with open(os.path.join(os.environ["RUNNER_TEMP"], "stub_args.txt"), "w") as fh:
    fh.write(" ".join(args))

for key, value in data.items():
    if quotes:
        print(f'{key.upper()}="{value}"')
    else:
        print(f"{key.upper()}={value}")
