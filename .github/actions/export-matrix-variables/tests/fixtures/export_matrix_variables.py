#!/usr/bin/env python3
"""Test stub for test-infra/.github/scripts/export_matrix_variables.py.

Reads a JSON matrix from --input-file and prints KEY=VALUE lines
(KEY upper-cased). With --add-quotes-around-value, values are wrapped
in double quotes.
"""
import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--add-quotes-around-value", action="store_true")
    args = parser.parse_args()
    with open(args.input_file) as f:
        matrix = json.load(f)
    for key, value in matrix.items():
        if args.add_quotes_around_value:
            print(f'{key.upper()}="{value}"')
        else:
            print(f"{key.upper()}={value}")


if __name__ == "__main__":
    main()
