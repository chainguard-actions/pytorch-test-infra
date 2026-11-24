<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia-windows/v20261123-205410** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a), direct expression interpolation: the 'Update NVIDIA driver' step puts a GitHub Actions expression straight into its cmd run script: `${{ github.action_path }}\..\..\scripts\driver_update.bat`. The value is pasted into the script before cmd parses it. Use the runner-provided environment variable instead, quoted: `"%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat"`.

Locations:

- `action.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In the 'Update NVIDIA driver' step (shell: cmd), I replaced the inline `${{ github.action_path }}` expression with the environment variable the runner already sets, in quotes: "%GITHUB_ACTION_PATH%\..\..\scripts\driver_update.bat". This is cmd syntax, so the step still runs under its shell. It still resolves to the same script path and is called the same way as upstream. Nothing was run to test it.

