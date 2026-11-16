#!/bin/sh
# Creates a fake `brew` on PATH and a fake brew prefix whose python<ver>
# binaries create a minimal venv. Logs calls for assertions.
set -e
FAKE="$RUNNER_TEMP/fake-brew"
rm -rf "$FAKE"
mkdir -p "$FAKE/bin" "$FAKE/prefix/bin"

cat > "$FAKE/bin/brew" <<'EOF'
#!/bin/sh
FAKE="$(cd "$(dirname "$0")/.." && pwd)"
echo "$*" >> "$FAKE/brew-calls.log"
case "$1" in
  --prefix) echo "$FAKE/prefix" ;;
esac
exit 0
EOF
chmod +x "$FAKE/bin/brew"

for v in 3.9 3.10 3.11 3.12 3.13; do
  cat > "$FAKE/prefix/bin/python$v" <<'EOF'
#!/bin/sh
FAKE="$(cd "$(dirname "$0")/../.." && pwd)"
echo "$*" >> "$FAKE/python-calls.log"
if [ "$1" = "-m" ] && [ "$2" = "venv" ]; then
  mkdir -p "$3/bin"
  cat > "$3/bin/python" <<'INNER'
#!/bin/sh
echo "$*" >> "$(dirname "$0")/../pip-calls.log"
exit 0
INNER
  chmod +x "$3/bin/python"
  exit 0
fi
exit 1
EOF
  chmod +x "$FAKE/prefix/bin/python$v"
done

echo "$FAKE/bin" >> "$GITHUB_PATH"
