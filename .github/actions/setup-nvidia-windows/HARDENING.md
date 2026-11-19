<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261118-220128** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): a GitHub Actions expression is placed directly inside a run: script. The offending line is `${{ github.action_path }}\..\..\scripts\driver_update.bat` in the cmd step 'Update NVIDIA driver'. The template is filled in before cmd parses the line, so the value never gets any shell quoting. To fix it, use the runner-provided %GITHUB_ACTION_PATH% env var (or pass the value through an env: entry) and quote it, for example "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat".

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml's cmd step 'Update NVIDIA driver', replaced the inline ${{ github.action_path }} expression with the runner-provided %GITHUB_ACTION_PATH% env var, quoted for cmd: "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat". Invocation semantics are otherwise unchanged.

