#!/bin/bash
# Installs fake aws/docker (and jq if missing) on PATH so the action can be
# exercised without AWS credentials or a real registry.
# Every call is logged to /tmp/fake-calls.log.
set -euo pipefail
BIN=/tmp/fakebin
rm -rf "$BIN"
mkdir -p "$BIN"
: > /tmp/fake-calls.log

cat > "$BIN/aws" <<'EOF'
#!/bin/bash
echo "aws $*" >> /tmp/fake-calls.log
rc="${FAKE_AWS_RC:-0}"
if [ "$rc" = "0" ]; then echo "fake-password"; fi
exit "$rc"
EOF

cat > "$BIN/docker" <<'EOF'
#!/bin/bash
echo "docker $*" >> /tmp/fake-calls.log
case "$1" in
  login) cat >/dev/null; echo "Login Succeeded"; exit "${FAKE_DOCKER_LOGIN_RC:-0}" ;;
  manifest) echo '{"config":{"size":1048576},"layers":[{"size":1048576}]}'; exit 0 ;;
  inspect) exit "${FAKE_DOCKER_INSPECT_RC:-1}" ;;
  pull) exit "${FAKE_DOCKER_PULL_RC:-0}" ;;
esac
exit 0
EOF

if ! command -v jq >/dev/null 2>&1; then
  cat > "$BIN/jq" <<'EOF'
#!/bin/bash
cat >/dev/null
echo 2
EOF
fi

chmod +x "$BIN"/*
echo "$BIN" >> "$GITHUB_PATH"
