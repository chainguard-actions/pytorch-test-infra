<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261103-202628** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) is violated: a GitHub Actions expression is placed directly inside a run: block. The 'Update NVIDIA driver' step (shell: cmd) runs `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The expression is filled in by template substitution before the shell parses the line. Use the runner env var instead, e.g. `"%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat"`, or pass the value through an env: variable and quote it.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Replaced the inline ${{ github.action_path }} expression in the cmd-shell 'Update NVIDIA driver' step with the runner env var, quoted: "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat". No other expressions remain in run blocks.

