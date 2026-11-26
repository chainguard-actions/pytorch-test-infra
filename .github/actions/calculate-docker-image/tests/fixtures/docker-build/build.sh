#!/bin/bash
# No-op fake docker build script used by tests. Records its arguments.
echo "fake build.sh called with: $*"
printf '%s\n' "$@" > /tmp/calc-docker-build-args.txt
exit 0
