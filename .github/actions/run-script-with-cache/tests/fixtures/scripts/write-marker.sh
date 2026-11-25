#!/usr/bin/env bash
set -euo pipefail
echo "pwd=$(pwd)" > "${GITHUB_WORKSPACE}/script-marker.txt"
echo "buildvar=${TEST_BUILD_ENV_VAR:-unset}" >> "${GITHUB_WORKSPACE}/script-marker.txt"
echo "script ran"
