#!/usr/bin/env python3
"""Test stand-in for test-infra/.github/scripts/export_matrix_variables.py."""
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--input-file", required=True)
parser.add_argument("--add-quotes-around-value", action="store_true")
args = parser.parse_args()

with open(args.input_file) as f:
    matrix = json.load(f)

print("ADD_QUOTES_FLAG=" + ("yes" if args.add_quotes_around_value else "no"))
for key, value in matrix.items():
    name = key.upper().replace("-", "_")
    if args.add_quotes_around_value:
        print(f'{name}="{value}"')
    else:
        print(f"{name}={value}")
