#!/usr/bin/env bash
# Installs fake `aws` and `docker` binaries on PATH (via GITHUB_PATH).
# Every invocation is logged to $MOCK_LOG.
# Behavior knobs (env vars visible to the action step):
#   MOCK_INSPECT_EXIT - exit code of `docker inspect` (default 1 => image not local)
#   MOCK_PULL_EXIT    - exit code of `docker pull` (default 0)
set -euo pipefail

MOCK_BIN=/tmp/mockbin
MOCK_LOG="${MOCK_LOG:-/tmp/mock-calls.log}"
mkdir -p "$MOCK_BIN"
: > "$MOCK_LOG"

cat > "$MOCK_BIN/aws" <<'EOF'
#!/bin/sh
echo "aws $*" >> "${MOCK_LOG:-/tmp/mock-calls.log}"
echo "fake-ecr-password"
exit 0
EOF

cat > "$MOCK_BIN/docker" <<'EOF'
#!/bin/sh
echo "docker $*" >> "${MOCK_LOG:-/tmp/mock-calls.log}"
case "$1" in
  login)
    cat > /dev/null
    echo "Login Succeeded"
    exit 0
    ;;
  manifest)
    echo '{"config":{"size":1048576},"layers":[{"size":2097152},{"size":1048576}]}'
    exit 0
    ;;
  inspect)
    exit "${MOCK_INSPECT_EXIT:-1}"
    ;;
  pull)
    exit "${MOCK_PULL_EXIT:-0}"
    ;;
esac
exit 0
EOF

chmod +x "$MOCK_BIN/aws" "$MOCK_BIN/docker"
echo "$MOCK_BIN" >> "$GITHUB_PATH"
echo "Mocks installed in $MOCK_BIN, log at $MOCK_LOG"
