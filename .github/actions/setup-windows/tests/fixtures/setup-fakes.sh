#!/usr/bin/env bash
# Installs fake Windows/EC2 tooling on PATH so the Windows-only composite
# action can run on a Linux act runner:
#  - powershell: no-op that logs invocations (registry / Defender steps)
#  - cygpath:    identity path conversion
#  - curl:       serves canned EC2 metadata for 169.254.169.254, honors -o,
#                falls through to the real curl for everything else
set -euo pipefail

FAKEBIN="${RUNNER_TEMP:-/tmp}/fakebin"
mkdir -p "$FAKEBIN"
LOGDIR="${RUNNER_TEMP:-/tmp}/fakelogs"
mkdir -p "$LOGDIR"
: > "$LOGDIR/powershell.log"
: > "$LOGDIR/curl.log"

REAL_CURL="$(command -v curl || echo /usr/bin/curl)"

cat > "$FAKEBIN/powershell" <<EOF
#!/usr/bin/env bash
echo "powershell \$*" >> "$LOGDIR/powershell.log"
exit 0
EOF

cat > "$FAKEBIN/cygpath" <<'EOF'
#!/usr/bin/env bash
# print the last argument unchanged
for last in "$@"; do :; done
echo "${last:-}"
EOF

cat > "$FAKEBIN/curl" <<EOF
#!/usr/bin/env bash
out=""
prev=""
for arg in "\$@"; do
  case "\$prev" in
    -o|--output) out="\$arg" ;;
  esac
  prev="\$arg"
done
case "\$*" in
  *169.254.169.254*)
    echo "curl \$*" >> "$LOGDIR/curl.log"
    payload="fake-token"
    case "\$*" in
      *meta-data/ami-id*) payload="ami-fake123" ;;
      *meta-data/instance-id*) payload="i-fake456" ;;
      *meta-data/instance-type*) payload="c5.fake" ;;
    esac
    if [ -n "\$out" ]; then
      printf '%s' "\$payload" > "\$out"
    else
      printf '%s' "\$payload"
    fi
    exit 0
    ;;
esac
exec "$REAL_CURL" "\$@"
EOF

chmod +x "$FAKEBIN/powershell" "$FAKEBIN/cygpath" "$FAKEBIN/curl"
echo "$FAKEBIN" >> "$GITHUB_PATH"
echo "Installed fakes into $FAKEBIN"
