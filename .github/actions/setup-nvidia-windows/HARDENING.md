<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): a GitHub Actions expression is placed directly inside a run: script. The offending line is `${{ github.action_path }}\..\..\scripts\driver_update.bat`, in the 'Update NVIDIA driver' step (shell: cmd). Fix: add `env: ACTION_PATH: ${{ github.action_path }}` to the step and call `"%ACTION_PATH%\..\..\scripts\driver_update.bat"` in the script. The quotes are part of the fix.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In the 'Update NVIDIA driver' step (shell: cmd), I moved ${{ github.action_path }} into env as ACTION_PATH. The script now calls "%ACTION_PATH%\..\..\scripts\driver_update.bat" using quoted cmd syntax.

