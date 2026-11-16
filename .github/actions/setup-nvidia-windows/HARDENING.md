<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violated: a GitHub Actions expression is placed directly inside a run: script in the 'Update NVIDIA driver' step (shell: cmd). Offending line: `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The template is substituted before cmd parses the script. Fix: pass the value through env (e.g. env: ACTION_PATH: ${{ github.action_path }}) and use the quoted form in the script: "%ACTION_PATH%\..\..\scripts\driver_update.bat".

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Moved github.action_path into env ACTION_PATH for the 'Update NVIDIA driver' cmd step and invoke it as "%ACTION_PATH%\..\..\scripts\driver_update.bat" (quoted, cmd syntax). The relative script path is unchanged.

