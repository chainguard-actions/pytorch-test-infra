#!/usr/bin/env bash
# Fake docker build script used by tests: records its arguments instead of building.
set -e
echo "fake build.sh called with: $*"
printf '%s\n' "$@" > "${GITHUB_WORKSPACE}/fake-build-args.txt"
