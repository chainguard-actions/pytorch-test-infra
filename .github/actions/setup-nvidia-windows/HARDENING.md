<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261125-022556** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): a GitHub Actions expression is placed directly inside a run: script. The offending line in the 'Update NVIDIA driver' step (shell: cmd) is `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The expression is filled into the script text before cmd runs it. Fix: use the runner-provided environment variable instead, e.g. `"%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat"`.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the 'Update NVIDIA driver' step (shell: cmd) no longer puts ${{ github.action_path }} into the script text. It now runs "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat", using the environment variable the runner sets. The path is in quotes so a space in it doesn't break the command. Not tested here, since that needs a Windows GPU runner.

