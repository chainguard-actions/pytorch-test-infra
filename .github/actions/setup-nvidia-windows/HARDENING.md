<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): a GitHub Actions expression is placed directly inside a run: block in the 'Update NVIDIA driver' step (shell: cmd). The offending line is `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The expression is filled in by the template before cmd parses the line. Fix: use the runner-provided env var instead, written as "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat" (quoted).

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the 'Update NVIDIA driver' step (shell: cmd) no longer puts ${{ github.action_path }} directly into the script. It now runs "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat", using the env var the runner already sets, in quotes, with the same relative path as before. cmd now expands the path when it runs the line. Before, GitHub pasted the text into the script before cmd parsed it. I didn't change anything else, and I haven't run the action to test this.

