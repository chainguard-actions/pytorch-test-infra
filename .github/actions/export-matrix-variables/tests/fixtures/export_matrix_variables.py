#!/usr/bin/env python3
"""Stand-in for pytorch/test-infra's export_matrix_variables.py used by tests.

Reads a JSON object from --input-file and prints KEY=VALUE lines (uppercased
keys), quoting values when --add-quotes-around-value is given.
"""
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--input-file", required=True)
parser.add_argument("--add-quotes-around-value", action="store_true")
args = parser.parse_args()

with open(args.input_file) as f:
    data = json.load(f)

print(f"QUOTES_FLAG={'yes' if args.add_quotes_around_value else 'no'}")
for key, value in data.items():
    if args.add_quotes_around_value:
        print(f'{key.upper()}="{value}"')
    else:
        print(f"{key.upper()}={value}")
