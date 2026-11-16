<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261029-163400** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) is violated: a GitHub Actions expression is placed directly inside a run: script. The offending line in the 'Update NVIDIA driver' step is `${{ github.action_path }}\..\..\scripts\driver_update.bat`. To fix it, set an env var such as ACTION_PATH: ${{ github.action_path }}, or use the runner-provided GITHUB_ACTION_PATH variable, and call the script as "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat" (quoted, because this step uses shell: cmd).

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In the 'Update NVIDIA driver' step (shell: cmd), I replaced the inline ${{ github.action_path }} with the runner-provided %GITHUB_ACTION_PATH% variable and put the script path in quotes. The relative path (..\..\scripts\driver_update.bat) is unchanged from upstream. Not tested.

