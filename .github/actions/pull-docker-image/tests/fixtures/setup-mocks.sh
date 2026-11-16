#!/usr/bin/env bash
# Installs fake `aws` and `docker` binaries on PATH that record their invocations.
# Behaviour toggles (files):
#   /tmp/fake-docker/image-present  -> `docker inspect --type=image` succeeds
#   /tmp/fake-docker/pull-fail      -> `docker pull` fails
set -euo pipefail

MOCK_BIN="${RUNNER_TEMP:-/tmp}/fake-bin"
mkdir -p "$MOCK_BIN" /tmp/fake-docker
rm -f /tmp/fake-docker/*.log

cat > "$MOCK_BIN/aws" <<'EOF'
#!/usr/bin/env bash
echo "aws $*" >> /tmp/fake-docker/aws.log
if [ "$1" = "ecr" ] && [ "$2" = "get-login-password" ]; then
  echo "fake-ecr-password"
  exit 0
fi
exit 0
EOF

cat > "$MOCK_BIN/docker" <<'EOF'
#!/usr/bin/env bash
echo "docker $*" >> /tmp/fake-docker/calls.log
case "$1" in
  login)
    cat > /tmp/fake-docker/login-stdin.log
    echo "Login Succeeded"
    exit 0
    ;;
  manifest)
    cat <<'JSON'
{"schemaVersion":2,"config":{"size":1048576},"layers":[{"size":2097152},{"size":1048576}]}
JSON
    exit 0
    ;;
  inspect)
    if [ -f /tmp/fake-docker/image-present ]; then
      echo '[{"Id":"sha256:fake"}]'
      exit 0
    fi
    echo "Error: No such image" >&2
    exit 1
    ;;
  pull)
    if [ -f /tmp/fake-docker/pull-fail ]; then
      echo "Error: pull failed" >&2
      exit 1
    fi
    echo "Pulled $2"
    exit 0
    ;;
esac
exit 0
EOF

chmod +x "$MOCK_BIN/aws" "$MOCK_BIN/docker"
echo "$MOCK_BIN" >> "$GITHUB_PATH"
