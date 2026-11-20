#!/usr/bin/env bash
# Creates mock binaries (curl, aws, docker, sudo, systemctl, lspci) so the
# EC2-oriented action can run under act without real AWS/EC2/Docker access.
set -euo pipefail
MOCK="${RUNNER_TEMP}/mockbin"
LOG="${RUNNER_TEMP}/mock-calls.log"
mkdir -p "$MOCK"
: > "$LOG"

cat > "$MOCK/curl" <<EOF
#!/usr/bin/env bash
echo "curl \$*" >> "$LOG"
out=""; prev=""
for a in "\$@"; do
  case "\$prev" in -o|--output) out="\$a" ;; esac
  prev="\$a"
done
case "\$*" in
  *api/token*) payload="fake-token" ;;
  *meta-data/ami-id*) payload="ami-0123456789abcdef0" ;;
  *meta-data/instance-id*) payload="i-0123456789abcdef0" ;;
  *meta-data/instance-type*) payload="c5.large" ;;
  *) payload="" ;;
esac
if [ -n "\$out" ]; then printf '%s' "\$payload" > "\$out"; else printf '%s' "\$payload"; fi
exit 0
EOF

cat > "$MOCK/aws" <<EOF
#!/usr/bin/env bash
echo "aws \$*" >> "$LOG"
case "\$*" in
  *get-caller-identity*)
    printf '{\n    "UserId": "AIDAEXAMPLE",\n    "Account": "123456789012",\n    "Arn": "arn:aws:iam::123456789012:user/test"\n}\n' ;;
  *get-login-password*) echo "fake-ecr-password" ;;
esac
exit 0
EOF

cat > "$MOCK/docker" <<EOF
#!/usr/bin/env bash
echo "docker \$*" >> "$LOG"
case "\$1" in
  login)
    pw="\$(cat)"
    echo "docker-login-password \$pw" >> "$LOG"
    echo "Login Succeeded" ;;
  ps) ;;
  version) echo "Docker version mock" ;;
esac
exit 0
EOF

cat > "$MOCK/sudo" <<EOF
#!/usr/bin/env bash
echo "sudo \$*" >> "$LOG"
exec "\$@"
EOF

cat > "$MOCK/systemctl" <<EOF
#!/usr/bin/env bash
echo "systemctl \$*" >> "$LOG"
exit 0
EOF

cat > "$MOCK/lspci" <<EOF
#!/usr/bin/env bash
echo "lspci \$*" >> "$LOG"
echo "00:00.0 Host bridge: Intel Corporation 440FX"
exit 0
EOF

chmod +x "$MOCK"/*
echo "$MOCK" >> "$GITHUB_PATH"
