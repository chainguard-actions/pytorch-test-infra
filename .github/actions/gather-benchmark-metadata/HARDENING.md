<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the expression ${{ inputs.venv }} is placed directly inside the 'Gather the metadata' run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is pasted into the script before the shell runs, so a crafted venv input can run arbitrary commands. Fix: map it to an env var (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

A composite step uses a branch ref instead of a commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a full 40-character commit SHA.

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

Moved inputs.venv into a VENV env var and referenced it as "${VENV}" in the run script. Pinned pytorch/test-infra/.github/actions/get-workflow-job-id from @main to the upstream commit 6f7274a0eff04dd4f8ada574e4e144610cece2c8 (the commit this release was built from, verified via ls-remote).

