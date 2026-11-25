#!/usr/bin/env bash
# Provide a `powershell` command on Linux (act) that runs pwsh with stub
# definitions for Windows-only CIM cmdlets preloaded.
set -euo pipefail

STUBS="$GITHUB_WORKSPACE/tests/fixtures/ps-stubs.ps1"
echo "DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1" >> "$GITHUB_ENV"
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1

PWSH="$(command -v pwsh || true)"
if [ -z "$PWSH" ]; then
  case "$(uname -m)" in
    x86_64) arch=x64 ;;
    aarch64|arm64) arch=arm64 ;;
    *) echo "unsupported arch $(uname -m)"; exit 1 ;;
  esac
  ver=7.4.6
  dest="$HOME/.pwsh"
  mkdir -p "$dest"
  url="https://github.com/PowerShell/PowerShell/releases/download/v${ver}/powershell-${ver}-linux-${arch}.tar.gz"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$url" -o /tmp/pwsh.tar.gz
  else
    wget -q "$url" -O /tmp/pwsh.tar.gz
  fi
  tar -xzf /tmp/pwsh.tar.gz -C "$dest"
  chmod +x "$dest/pwsh"
  PWSH="$dest/pwsh"
fi
"$PWSH" -NoLogo -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'

shim="$HOME/.ps-shim"
mkdir -p "$shim"
cat > "$shim/powershell" <<EOF
#!/usr/bin/env bash
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
case "\${1:-}" in
  -command|-Command|-c|-C) shift ;;
esac
exec "$PWSH" -NoLogo -NoProfile -Command ". '$STUBS'; \$*"
EOF
chmod +x "$shim/powershell"
echo "$shim" >> "$GITHUB_PATH"
echo "powershell shim installed at $shim/powershell"
