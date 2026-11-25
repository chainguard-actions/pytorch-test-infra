<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261119-192116** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a), direct expression interpolation. The 'Gather the metadata' step puts ${{ inputs.venv }} straight into the run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The expression is filled in before bash parses the script, so a crafted venv value can break out of the quotes and run commands. Fix: pass it through env (VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

A uses: reference points to a mutable branch instead of a 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

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

I moved inputs.venv into the env: block of the 'Gather the metadata' step as VENV. The script now uses "${VENV}" in both places where the expression used to be pasted in. I pinned pytorch/test-infra/.github/actions/get-workflow-job-id to commit 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4, with '# main' kept as a comment. That is the upstream commit this mirror version was built from, so the sub-action matches this release rather than whatever main points to now. The lookup only confirmed the full SHA as I entered it; I didn't check that the sub-action's files exist at that commit. No tests were run.

