#!/bin/bash
# Fake docker build script used by tests. Records its arguments instead of building.
set -e
echo "fake build.sh called with: $*"
printf '%s\n' "$@" > /tmp/fake-build-args.txt
