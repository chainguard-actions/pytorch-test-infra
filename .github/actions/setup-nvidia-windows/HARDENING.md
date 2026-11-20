<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261119-192116** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) direct expression interpolation: the 'Update NVIDIA driver' step puts a GitHub Actions expression straight into the run: script: `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The expression is substituted into the script text before cmd parses it. Fix: pass the path in through env (for example, set ACTION_PATH from github.action_path) and reference it in the script as "%ACTION_PATH%\..\..\scripts\driver_update.bat", or use the runner's GITHUB_ACTION_PATH env var, quoted.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Moved github.action_path into the step's env as ACTION_PATH and invoked the batch script as "%ACTION_PATH%\..\..\scripts\driver_update.bat" (cmd syntax, quoted). Relative script location unchanged.

