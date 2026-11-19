<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-runners-info/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-runners-info/v20261118-220128** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): the 'Gather the runners information' step puts the expression ${{ inputs.venv }} straight into its run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script text before the shell runs, so a crafted input can break out of the quotes and run arbitrary commands. Fix: add `env: VENV: ${{ inputs.venv }}` to the step and use "$VENV" in the script.

Locations:

- `action.yml:72`
- `action.yml:73`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.venv }}" appears directly in run: block of step "Gather the runners information"; move to env: map

Locations:

- `action.yml:73`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.venv }}" appears directly in run: block of step "Gather the runners information"; move to env: map

Locations:

- `action.yml:74`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, static-inline-injection

**Notes:**

Moved ${{ inputs.venv }} into the step's env: block as VENV and referenced "$VENV" in the 'Gather the runners information' step.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In action.yml, the 'Get device type' step now strips newlines and carriage returns from DEVICE_TYPE before writing it to GITHUB_ENV: safe_device_type=$(printf '%s' "$DEVICE_TYPE" | tr -d '\n\r'), then echo "DEVICE_TYPE=$safe_device_type" >> "$GITHUB_ENV". Behaviour is otherwise the same as upstream. The script still runs under 'set -u', so if DEVICE_TYPE is never set it still fails as before. The step uses composite bash, which sets pipefail, so a failing printf still stops the step. I also put quotes around $GITHUB_ENV in the 'Get device name' step. That value is always a fixed word, so this is only tidying. Nothing was run to test the change.

