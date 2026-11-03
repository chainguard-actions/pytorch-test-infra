#!/bin/bash
# Fake docker build script used by tests. Records its arguments instead of building.
set -e
MARKER="${BUILD_MARKER:-/tmp/act-docker-build-marker}"
printf '%s\n' "$@" > "${MARKER}"
echo "fake build.sh called with: $*"
