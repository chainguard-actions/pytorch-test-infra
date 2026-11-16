#!/bin/bash
# Usage: setup-fakes.sh [normal|aws-fail|docker-down]
# Installs fake binaries (curl for EC2 metadata, aws, docker, sudo, systemctl,
# lspci) into a directory that is prepended to PATH via GITHUB_PATH.
set -euo pipefail
MODE="${1:-normal}"
FAKEBIN="/tmp/fakes-bin"
LOGDIR="/tmp/fakes-log"
rm -rf "$FAKEBIN" "$LOGDIR"
mkdir -p "$FAKEBIN" "$LOGDIR"

REALCURL="$(command -v curl || echo /usr/bin/curl)"

case "$MODE" in
  aws-fail) touch "$LOGDIR/aws-fail" ;;
  docker-down) touch "$LOGDIR/docker-down" ;;
esac

cat > "$FAKEBIN/curl" <<'EOF'
#!/bin/bash
echo "$*" >> /tmp/fakes-log/curl.log
case "$*" in
  *169.254.169.254/latest/api/token*) printf 'faketoken'; exit 0 ;;
  *169.254.169.254/latest/meta-data/*)
    cat=""
    for a in "$@"; do
      case "$a" in *meta-data/*) cat="${a##*/meta-data/}" ;; esac
    done
    case "$cat" in
      ami-id) printf 'ami-0fake' ;;
      instance-id) printf 'i-0fake' ;;
      instance-type) printf 'c5.fake' ;;
      *) exit 22 ;;
    esac
    exit 0 ;;
esac
exec __REALCURL__ "$@"
EOF
sed -i "s#__REALCURL__#${REALCURL}#" "$FAKEBIN/curl"

cat > "$FAKEBIN/aws" <<'EOF'
#!/bin/bash
echo "$*" >> /tmp/fakes-log/aws.log
if [ -f /tmp/fakes-log/aws-fail ]; then
  echo "Unable to locate credentials" >&2
  exit 255
fi
case "$1 $2" in
  "sts get-caller-identity")
    printf '{\n    "UserId": "AIDFAKE",\n    "Account": "123456789012",\n    "Arn": "arn:aws:iam::123456789012:user/fake"\n}\n' ;;
  "ecr get-login-password") echo "fakepass" ;;
  *) exit 1 ;;
esac
EOF

cat > "$FAKEBIN/docker" <<'EOF'
#!/bin/bash
echo "$*" >> /tmp/fakes-log/docker.log
case "$1" in
  version)
    if [ -f /tmp/fakes-log/docker-down ]; then exit 1; fi
    echo "fake docker"; exit 0 ;;
  login) cat > /tmp/fakes-log/docker-login-stdin; echo "Login Succeeded"; exit 0 ;;
  ps) exit 0 ;;
  stop) exit 1 ;;
  system) echo "Total reclaimed space: 0B"; exit 0 ;;
esac
exit 0
EOF

cat > "$FAKEBIN/sudo" <<'EOF'
#!/bin/bash
echo "$*" >> /tmp/fakes-log/sudo.log
exec "$@"
EOF

cat > "$FAKEBIN/systemctl" <<'EOF'
#!/bin/bash
echo "$*" >> /tmp/fakes-log/systemctl.log
case "$1" in
  is-active)
    if [ -f /tmp/fakes-log/docker-down ]; then exit 3; fi
    exit 0 ;;
esac
exit 0
EOF

cat > "$FAKEBIN/lspci" <<'EOF'
#!/bin/bash
echo "00:00.0 Host bridge: Fake Corporation Fake Host Bridge"
exit 0
EOF

chmod +x "$FAKEBIN"/*
echo "$FAKEBIN" >> "$GITHUB_PATH"
echo "Installed fakes in $FAKEBIN (mode=$MODE)"
