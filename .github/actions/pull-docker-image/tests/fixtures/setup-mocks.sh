#!/usr/bin/env bash
# Installs fake `aws` and `docker` binaries on PATH that log their invocations
# to /tmp/mock/*.log. Behavior is controlled by flag files in /tmp/mock:
#   image-local  -> `docker inspect` succeeds (image already present)
#   pull-fail    -> `docker pull` fails
#   login-fail   -> `docker login` fails
#   aws-fail     -> `aws ecr get-login-password` fails
set -euo pipefail

MOCK=/tmp/mock
rm -rf "$MOCK"
mkdir -p "$MOCK/bin"

cat > "$MOCK/bin/aws" <<'EOF'
#!/usr/bin/env bash
echo "aws $*" >> /tmp/mock/aws.log
if [ -f /tmp/mock/aws-fail ]; then
  echo "aws: simulated failure" >&2
  exit 255
fi
echo "fake-password"
EOF

cat > "$MOCK/bin/docker" <<'EOF'
#!/usr/bin/env bash
echo "docker $*" >> /tmp/mock/docker.log
case "$1" in
  login)
    cat > /dev/null
    [ -f /tmp/mock/login-fail ] && exit 1
    echo "Login Succeeded"
    exit 0
    ;;
  manifest)
    echo '{"config":{"size":1048576},"layers":[{"size":1048576},{"size":2097152}]}'
    exit 0
    ;;
  inspect)
    [ -f /tmp/mock/image-local ] && exit 0
    exit 1
    ;;
  pull)
    if [ -f /tmp/mock/pull-fail ]; then
      echo "Error: simulated pull failure" >&2
      exit 1
    fi
    echo "Pulled $2"
    exit 0
    ;;
esac
exit 0
EOF

chmod +x "$MOCK/bin/aws" "$MOCK/bin/docker"
touch "$MOCK/docker.log" "$MOCK/aws.log"
echo "$MOCK/bin" >> "$GITHUB_PATH"
