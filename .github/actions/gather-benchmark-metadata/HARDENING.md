<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261119-192116** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml points a composite step at a branch, not a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'. Whoever controls that branch can change the code this action runs. Pin it to a commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Sub-rule (a), direct expression interpolation, in the 'Gather the metadata' step. The run block puts ${{ inputs.venv }} straight into the shell script: 'if [[ -n "${{ inputs.venv }}" ]]; then' and 'source "${{ inputs.venv }}"'. The value is pasted into the script before the shell parses it, so a crafted input can break out of the quotes and run its own commands. Move inputs.venv into an env: variable (e.g. VENV) and use "$VENV" in the script.

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

Pinned pytorch/test-infra/.github/actions/get-workflow-job-id to commit 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4 (the upstream commit, checked with lookup_action_sha), with a '# main' comment. Moved inputs.venv into a VENV env var in the 'Gather the metadata' step; the script now uses "${VENV}".

