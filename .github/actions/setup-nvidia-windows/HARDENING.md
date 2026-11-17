<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation: the expression is placed directly inside a run: script. In the 'Update NVIDIA driver' step, line 11 reads `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The expression is filled in before the cmd shell runs, so its text becomes part of the command. Fix: use the runner-provided environment variable instead, e.g. `"%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat"`.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In the 'Update NVIDIA driver' step (shell: cmd), replaced the inline ${{ github.action_path }} expression with the runner-provided %GITHUB_ACTION_PATH% environment variable, quoted: "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat". Relative path and invocation otherwise unchanged.

