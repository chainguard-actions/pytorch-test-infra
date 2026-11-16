#!/bin/bash
# Fake docker build script used by tests. It should never actually be invoked
# because the tests mock `docker manifest inspect` to report the image exists.
set -ex
echo "fake build.sh invoked with: $*"
