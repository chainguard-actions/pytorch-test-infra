<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a), direct expression interpolation: the 'Update NVIDIA driver' step puts a GitHub Actions expression straight into the run: script: `${{ github.action_path }}\..\..\scripts\driver_update.bat`. Template substitution happens before cmd parses the line. Fix: set the path through the step's env: or use the built-in %GITHUB_ACTION_PATH% variable, and double-quote it, for example "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat".

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Replaced the inline ${{ github.action_path }} in the cmd step with the runner's built-in %GITHUB_ACTION_PATH% env var, double-quoted: "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat". Shell remains cmd; behavior otherwise unchanged.

