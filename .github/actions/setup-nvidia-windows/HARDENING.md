<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261109-192709** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation: the GitHub Actions expression is placed directly inside a run: script (shell: cmd) in the 'Update NVIDIA driver' step. Offending line: `${{ github.action_path }}\..\..\scripts\driver_update.bat`. Fix: pass the value through an env var (e.g. ACTION_PATH: ${{ github.action_path }}) and reference it quoted in the script, e.g. `call "%ACTION_PATH%\..\..\scripts\driver_update.bat"`. Alternatively, use the runner-provided GITHUB_ACTION_PATH env var: `call "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat"`.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

I fixed the script-injection finding in the 'Update NVIDIA driver' step of action.yml. The step runs under shell: cmd, so I moved ${{ github.action_path }} into the step's env as ACTION_PATH. The script now calls it by its quoted cmd path: call "%ACTION_PATH%\..\..\scripts\driver_update.bat". This line is the last one in the script, so using `call` gives the same exit code as upstream running the .bat directly. I haven't run anything. The repo's test fakes cmd on Linux and only checks that 'driver_update.bat' and 'scripts' appear in the command it was given, so a real Windows runner is the only thing that will confirm %ACTION_PATH% expands and the script starts.

