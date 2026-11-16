<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-runners-info/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-runners-info/v20261109-192709** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation in the 'Gather the runners information' step: the expression ${{ inputs.venv }} is placed directly inside the run: script, so its value is substituted into the script text before the shell runs. Offending lines: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. A venv value that contains a double quote, $(...) or backticks can break out of the string and run arbitrary commands. Fix: add `env: VENV: ${{ inputs.venv }}` to the step and use `if [[ -n "$VENV" ]]; then source "$VENV"; fi`.

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

Moved ${{ inputs.venv }} into env VENV in the 'Gather the runners information' step and referenced it as "$VENV".

