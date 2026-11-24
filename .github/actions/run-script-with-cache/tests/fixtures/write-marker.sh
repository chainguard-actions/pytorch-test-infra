#!/bin/bash
# Test fixture: records that it ran, the FOO env var, and the working dir.
echo "ran:${FOO:-unset}:$(pwd)" > "${RUNNER_TEMP}/marker.txt"
echo "ARG_COUNT=$#" >> "${RUNNER_TEMP}/marker.txt"
