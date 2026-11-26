<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-223308** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Gather the metadata' step puts the inputs.venv expression straight into the run: script, so the value is substituted into the shell source before bash parses it. Offending lines: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. Fix: add `VENV: ${{ inputs.venv }}` to the step's env: block and use `"$VENV"` in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

The composite step points at a branch instead of a full commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a 40-character commit SHA.

Locations:

- `action.yml:38`

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

**Fixes applied:** script-injection, static-inline-injection, unpinned-uses

**Notes:**

Moved inputs.venv into the step's env: block as VENV and switched the script to use "${VENV}". Pinned pytorch/test-infra/.github/actions/get-workflow-job-id to d50cbade0e174f113111122f50b7a814b9b4c61d. That is the upstream commit this version was built from, and lookup_action_sha confirmed it exists. The trailing comment still says # main.

