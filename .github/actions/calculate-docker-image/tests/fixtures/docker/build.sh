#!/bin/bash
# Fixture docker build script used by tests. It is never expected to be run
# because the fake docker reports the image as already existing.
echo "fake build.sh called with: $*"
exit 0
