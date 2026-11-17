<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261103-202628** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation: a GitHub Actions expression is placed directly inside a run: script. Offending line: `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The expression is filled in by template substitution before the cmd shell parses the line. Use the runner-provided environment variable in quotes instead, e.g. `"%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat"`.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the 'Update NVIDIA driver' step (shell: cmd) now runs "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat" instead of putting ${{ github.action_path }} directly in the script. The path is quoted so cmd reads it as one argument. GITHUB_ACTION_PATH is set by the runner and points to the same directory, so the script resolves as before. Not tested by running the action.

