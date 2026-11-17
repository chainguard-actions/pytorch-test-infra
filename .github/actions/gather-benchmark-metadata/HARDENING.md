<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261021-234439** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Gather the metadata' step puts the expression ${{ inputs.venv }} straight into the run: script, in `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script before the shell runs it, so a crafted venv input can inject shell commands. Fix: pass it through an env var (VENV: ${{ inputs.venv }}) and reference it double-quoted as "$VENV".

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

A composite step uses a mutable branch ref instead of a full commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

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

Moved inputs.venv into an env var (VENV) and referenced it as "${VENV}". Pinned get-workflow-job-id to upstream commit 4bb924e6cddf98370d0c754d6769b492fe457233 (the upstream_ref this mirror was built from) with a '# main' comment.

