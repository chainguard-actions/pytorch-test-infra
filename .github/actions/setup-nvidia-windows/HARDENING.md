<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261021-234439** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) is broken: a GitHub Actions expression is placed straight into a run: script. The 'Update NVIDIA driver' step (shell: cmd) has the line `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The template is filled in before cmd reads the line. To fix it, pass the value through an env: variable (for example ACTION_PATH: ${{ github.action_path }}) and use it in quotes as "%ACTION_PATH%\..\..\scripts\driver_update.bat". You could also use the runner's GITHUB_ACTION_PATH env var.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Moved ${{ github.action_path }} into the step's env: block as ACTION_PATH. The cmd step now runs "%ACTION_PATH%\..\..\scripts\driver_update.bat" with the path in quotes, so the expression is no longer pasted into the script text. I haven't run the changed step.

