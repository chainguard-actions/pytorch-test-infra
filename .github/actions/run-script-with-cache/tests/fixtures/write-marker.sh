#!/bin/bash
set -eu
echo "script running in $(pwd)"
echo "${MARKER_VALUE}" > /tmp/action-marker.txt
pwd > /tmp/action-pwd.txt
