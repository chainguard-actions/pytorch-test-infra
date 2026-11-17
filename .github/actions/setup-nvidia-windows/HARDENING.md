<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): a GitHub Actions expression is placed straight into a run: script in the 'Update NVIDIA driver' step: `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The check fails any ${{ }} expression inside a run: script, whatever context it reads from. To fix it, use the GITHUB_ACTION_PATH environment variable instead, or set it in an env: block. In this cmd shell that means `"%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat"`.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the 'Update NVIDIA driver' step (shell: cmd) no longer puts `${{ github.action_path }}` inside the run: script. It now reads the runner's built-in GITHUB_ACTION_PATH variable in cmd syntax, quoted: "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat". The relative path is the same as upstream, and the batch file still runs as the step's last command, as before. Nothing was run to test this. The scripts/driver_update.bat file is not in this action directory; like upstream, the step expects it two levels above the action's own folder.

