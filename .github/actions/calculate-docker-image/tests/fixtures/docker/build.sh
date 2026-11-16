#!/usr/bin/env bash
# Fake docker build script used by tests: records its arguments instead of building.
set -e
echo "$@" > /tmp/fake-docker-build-args.txt
echo "fake build invoked with: $*"
