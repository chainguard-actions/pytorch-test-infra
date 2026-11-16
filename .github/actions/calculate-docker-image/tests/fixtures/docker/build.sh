#!/bin/bash
# Fake docker build script used by tests: records its arguments instead of building.
echo "$@" > /tmp/fake-build-args.txt
echo "fake build invoked with: $*"
