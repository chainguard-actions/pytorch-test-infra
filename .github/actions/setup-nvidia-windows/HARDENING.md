<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation: a GitHub Actions expression is placed directly inside a run: script. Offending line: `${{ github.action_path }}\..\..\scripts\driver_update.bat` in the 'Update NVIDIA driver' step (shell: cmd). The expression is substituted into the script text before cmd parses it. Fix: pass the path in through an env var (e.g. env: ACTION_PATH: ${{ github.action_path }}) and call "%ACTION_PATH%\..\..\scripts\driver_update.bat" with quotes, or use the GITHUB_ACTION_PATH variable that the runner already sets.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Moved ${{ github.action_path }} out of the cmd run script into env ACTION_PATH; the step now runs "%ACTION_PATH%\..\..\scripts\driver_update.bat" (quoted, cmd syntax). The relative path to the script is unchanged.

