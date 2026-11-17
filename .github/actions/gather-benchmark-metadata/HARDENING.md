<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261109-192709** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step references an action by a mutable branch instead of a 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Sub-rule (a) applies: an expression is placed directly in the run: script of the 'Gather the metadata' step. Offending lines: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. A crafted `venv` input can break out of the quotes and run arbitrary commands. Fix: pass the value through env (for example `VENV: ${{ inputs.venv }}`) and reference it as "$VENV".

Locations:

- `action.yml:57`
- `action.yml:58`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.venv }}" appears directly in run: block of step "Gather the metadata"; move to env: map

Locations:

- `action.yml:57`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.venv }}" appears directly in run: block of step "Gather the metadata"; move to env: map

Locations:

- `action.yml:58`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection

**Notes:**

Pinned the get-workflow-job-id action to 0569df511711f70601c984fe3a93dac324afc9ce. That is the upstream commit this mirror was built from, and I confirmed it exists with lookup_action_sha. The '# main' comment keeps the original ref readable. Moved inputs.venv into the step's env: as VENV and changed the run script to read "${VENV}" in both the -n test and the source line. The step behaves the same when venv is empty. Nothing was tested or run; a fresh analysis pass hasn't been done yet.

