<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261021-234439** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation: a GitHub Actions expression is placed directly inside a run: script (shell: cmd) in the 'Update NVIDIA driver' step. Offending line: `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The value is pasted into the script text before cmd parses it. Fix: use the runner-provided environment variable instead, e.g. `"%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat"`.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In the 'Update NVIDIA driver' step (shell: cmd) of action.yml, I replaced the inline `${{ github.action_path }}` with the runner's environment variable, quoted: "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat". The relative path to the script is unchanged. Nothing was run to test it. The step still runs only the .bat file, so leaving out `call` has no effect, same as upstream.

