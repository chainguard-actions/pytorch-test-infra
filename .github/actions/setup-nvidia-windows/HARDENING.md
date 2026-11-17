<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261029-163400** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): the 'Update NVIDIA driver' step puts a GitHub Actions expression straight into a run: script (shell: cmd): `${{ github.action_path }}\..\..\scripts\driver_update.bat`. Template substitution happens before the shell runs, so whatever the expression holds becomes part of the cmd command. Use the runner-provided env var instead, quoted: `"%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat"`.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the 'Update NVIDIA driver' step (shell: cmd) now calls the script using the runner's environment variable instead of the inline expression: "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat". The path is quoted, and the relative path stays the same as upstream. Not run or tested. I didn't check that ..\..\scripts\driver_update.bat is present in the published layout.

