#!/usr/bin/env bash
set -euo pipefail
echo "${MARKER_VALUE:-unset}" > "${GITHUB_WORKSPACE}/marker.txt"
pwd > "${GITHUB_WORKSPACE}/pwd.txt"
mkdir -p "${GITHUB_WORKSPACE}/cache-dir"
echo "cached" > "${GITHUB_WORKSPACE}/cache-dir/data.txt"
