<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20260922-155642** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that points to a branch, not a full commit SHA: 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'. Pin it to a 40-character commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a) is violated in the 'Gather the metadata' step. The expression ${{ inputs.venv }} is placed straight into the run: script: 'if [[ -n "${{ inputs.venv }}" ]]; then' and 'source "${{ inputs.venv }}"'. Move it into an env: variable (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

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

Pinned pytorch/test-infra/.github/actions/get-workflow-job-id to 28dee7456d0348d74a5faa85098bb028b263ee2b (the upstream commit this mirror was built from, so the sub-action matches the version of the code; '# main' comment kept). Moved inputs.venv into the step's env as VENV and referenced it as "${VENV}" in the Gather the metadata step.

