<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-223308** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite step uses a mutable branch ref instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a) violated: the 'Gather the metadata' step puts an expression directly inside its run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The input text is pasted into the script before the shell runs, so an attacker-supplied venv value can inject commands. Fix: pass it in through an env: variable (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

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

Pinned pytorch/test-infra/.github/actions/get-workflow-job-id to d50cbade0e174f113111122f50b7a814b9b4c61d (resolved main, same as upstream_commit). Moved inputs.venv into env VENV and referenced as "${VENV}" in the run script.

