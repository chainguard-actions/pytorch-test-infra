<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261125-223308** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation: a GitHub Actions expression is placed directly inside a run: block. The offending line is `${{ github.action_path }}\..\..\scripts\driver_update.bat` in the 'Update NVIDIA driver' step (shell: cmd). The value is filled into the script before cmd runs it. Fix: use the runner-provided %GITHUB_ACTION_PATH% env var instead, or pass the value in through the step's env: block and quote it, e.g. "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat".

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In the 'Update NVIDIA driver' step (shell: cmd), I replaced the inline ${{ github.action_path }} expression with the GITHUB_ACTION_PATH environment variable that the runner already sets. The line is now "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat", in quotes so a path with spaces still works. I kept upstream's way of starting the script (no `call`), so it runs the same as before. Nothing was run to test this.

