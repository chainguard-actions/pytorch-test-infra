<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-runners-info/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-runners-info/v20261021-234439** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) broken: the 'Gather the runners information' step puts the `${{ inputs.venv }}` expression straight into its run: script, in `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script text before bash parses it, so a crafted venv input can break out of the quotes and run any command. Fix: pass it in through an env var (e.g. `env: VENV: ${{ inputs.venv }}`) and refer to it as "$VENV".

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

Moved inputs.venv into the step's env: block as VENV and referenced as "$VENV" in the 'Gather the runners information' step.

