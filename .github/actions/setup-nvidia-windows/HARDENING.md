<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261109-192709** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): a GitHub Actions expression is placed straight into the run: script of the 'Update NVIDIA driver' step: `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The value is pasted into the cmd script before the shell runs, so special characters in the path are parsed as commands. Fix: pass the path through an env var (for example, env: ACTION_PATH: ${{ github.action_path }}) and call it as "%ACTION_PATH%\..\..\scripts\driver_update.bat". Under cmd, the runner also sets GITHUB_ACTION_PATH, so "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat" works too.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Moved ${{ github.action_path }} out of the cmd run: script in the 'Update NVIDIA driver' step. It is now set in the step's env: as ACTION_PATH, and the step runs "%ACTION_PATH%\..\..\scripts\driver_update.bat". The path is quoted so a path with spaces still runs. The script is still invoked directly, the same way upstream did. Nothing else changed.

