<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-runners-info/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-runners-info/v20261125-022556** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Gather the runners information' step puts `${{ inputs.venv }}` straight into the run script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script before the shell reads it, so a crafted venv input can break out of the quotes and run its own commands. Fix: pass it in through an env var, e.g. `env: VENV: ${{ inputs.venv }}`, and refer to it as "$VENV".

Locations:

- `action.yml:72`
- `action.yml:73`

### github-env-injection (severity: high)

The 'Get device type' step runs `echo "DEVICE_TYPE=$DEVICE_TYPE" >> $GITHUB_ENV` without first passing the value through `printf '%s' ... | tr -d '\n\r'`. DEVICE_TYPE comes from command output (nvidia-smi, rocminfo, hl-smi, lscpu), not a literal. It is also only set inside the if/elif branches, so if no branch matches, the value written is whatever DEVICE_TYPE the calling workflow passed in. A value containing a newline could add extra variables to GITHUB_ENV. Fix: `safe=$(printf '%s' "$DEVICE_TYPE" | tr -d '\n\r'); echo "DEVICE_TYPE=$safe" >> "$GITHUB_ENV"`.

Locations:

- `action.yml:64`

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

**Fixes applied:** script-injection, static-inline-injection, github-env-injection

**Notes:**

In action.yml, the 'Gather the runners information' step no longer puts `inputs.venv` straight into the script. It now goes through an `env: VENV` entry and the script uses "$VENV" in both places. The 'Get device type' step now strips newlines from DEVICE_TYPE with printf | tr -d '\n\r' before writing it to GITHUB_ENV, and "$GITHUB_ENV" is quoted. The step still exits under set -u when no branch sets DEVICE_TYPE, as upstream did, because the variable is referenced the same way. Nothing was run or tested.

