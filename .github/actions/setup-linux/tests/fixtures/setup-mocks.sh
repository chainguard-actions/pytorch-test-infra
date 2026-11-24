#!/usr/bin/env bash
# Install fake aws/docker/curl/sudo/lspci/systemctl on PATH so the action can
# run under act without EC2 metadata, AWS credentials or a docker daemon.
set -euo pipefail

FAKEBIN="${RUNNER_TEMP}/fakebin"
LOG="${RUNNER_TEMP}/mock-calls.log"
mkdir -p "$FAKEBIN"
: > "$LOG"

REAL_CURL="$(command -v curl || true)"

cat > "$FAKEBIN/curl" <<EOF
#!/usr/bin/env bash
echo "curl \$*" >> "$LOG"
case "\$*" in
  *169.254.169.254/latest/api/token*) echo "fake-token"; exit 0 ;;
  *169.254.169.254/latest/meta-data/ami-id*) echo "ami-0123456789abcdef0"; exit 0 ;;
  *169.254.169.254/latest/meta-data/instance-id*) echo "i-0123456789abcdef0"; exit 0 ;;
  *169.254.169.254/latest/meta-data/instance-type*) echo "c5.large"; exit 0 ;;
  *169.254.169.254*) echo "unknown"; exit 0 ;;
esac
if [ -n "$REAL_CURL" ]; then exec "$REAL_CURL" "\$@"; fi
exit 1
EOF

cat > "$FAKEBIN/aws" <<EOF
#!/usr/bin/env bash
echo "aws \$*" >> "$LOG"
case "\$1 \$2" in
  "sts get-caller-identity")
    cat <<'JSON'
{
    "UserId": "AIDAEXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/test"
}
JSON
    ;;
  "ecr get-login-password")
    echo "fake-ecr-password" ;;
  *) exit 1 ;;
esac
EOF

cat > "$FAKEBIN/docker" <<EOF
#!/usr/bin/env bash
echo "docker \$*" >> "$LOG"
case "\$1" in
  login)
    pw="\$(cat)"
    echo "docker-login-password \$pw" >> "$LOG"
    echo "Login Succeeded" ;;
  version|stop|system) exit 0 ;;
  ps) exit 0 ;;
  *) exit 0 ;;
esac
EOF

cat > "$FAKEBIN/sudo" <<EOF
#!/usr/bin/env bash
echo "sudo \$*" >> "$LOG"
exec "\$@"
EOF

cat > "$FAKEBIN/lspci" <<EOF
#!/usr/bin/env bash
echo "lspci \$*" >> "$LOG"
echo "00:00.0 Host bridge: Intel Corporation 440FX"
EOF

cat > "$FAKEBIN/systemctl" <<EOF
#!/usr/bin/env bash
echo "systemctl \$*" >> "$LOG"
exit 0
EOF

chmod +x "$FAKEBIN"/*
echo "$FAKEBIN" >> "$GITHUB_PATH"
echo "MOCK_LOG=$LOG" >> "$GITHUB_ENV"
