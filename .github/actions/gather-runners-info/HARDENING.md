<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-runners-info/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-runners-info/v20261125-223308** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Gather the runners information' step puts the input expression `${{ inputs.venv }}` straight into the run: script, on `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The expression is substituted into the script text before bash runs, so a value containing `"` or `$(...)` can execute commands. Fix: set `VENV: ${{ inputs.venv }}` in the step's env: block and use `"$VENV"` in the script.

Locations:

- `action.yml:74`
- `action.yml:75`

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

Moved ${{ inputs.venv }} into the step env as VENV and referenced "$VENV" in the run script of 'Gather the runners information'.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In action.yml, the 'Get device type' step now removes newlines and carriage returns from DEVICE_TYPE before writing it to $GITHUB_ENV, using safe=$(printf '%s' "$DEVICE_TYPE" | tr -d '\n\r'). This means a multi-line value can no longer add extra variables to the environment. I also put quotes around $GITHUB_ENV in both places it is written to. I haven't run the action after the change. Upstream's 'set -eux' is unchanged, so if DEVICE_NAME matches no branch and DEVICE_TYPE is unset, the step should still stop with an error as it did before.

