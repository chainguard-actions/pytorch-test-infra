#!/usr/bin/env bash
# Stand-in for "powershell" on act's Linux runner.
# act runs: powershell -command . '<script.ps1>'
# The shim records the script, then runs it with pwsh if pwsh is installed.
# Windows-only CIM cmdlets are stubbed so they return no sessions.
LOG="${POWERSHELL_SHIM_LOG:-/tmp/powershell-shim.log}"
script="${!#}"
script="${script#\'}"
script="${script%\'}"
script="${script#.}"
script="${script# }"
script="${script#\'}"
script="${script%\'}"

{
  echo "=== INVOCATION: $* ==="
  echo "script: $script"
  if [ -f "$script" ]; then cat "$script"; else echo "MISSING SCRIPT FILE"; fi
  echo "=== END ==="
} >> "$LOG"

if [ ! -f "$script" ]; then
  echo "powershell shim: script file not found: $script" >&2
  exit 1
fi

if command -v pwsh >/dev/null 2>&1; then
  echo "powershell shim: executing with pwsh (with CIM stubs)"
  echo "MODE: pwsh" >> "$LOG"
  exec pwsh -NoProfile -NonInteractive -Command "function Get-CimInstance { }; function Get-CimAssociatedInstance { process { } }; . '$script'"
fi

echo "powershell shim: pwsh is not installed, so the script was only recorded"
echo "MODE: recorded-only" >> "$LOG"
exit 0
