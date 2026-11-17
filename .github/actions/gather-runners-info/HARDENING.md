<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-runners-info/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-runners-info/v20261027-001733** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Gather the runners information' step puts the `${{ inputs.venv }}` expression straight into the run: script, on these lines: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is pasted in before the shell runs, so a crafted input can break out of the quotes and run its own commands. Fix: map it with `env: VENV: ${{ inputs.venv }}` and use `"$VENV"` in the script.

Locations:

- `action.yml:73`
- `action.yml:74`

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

Moved inputs.venv into the step env as VENV and referenced "$VENV" in the 'Gather the runners information' step.

