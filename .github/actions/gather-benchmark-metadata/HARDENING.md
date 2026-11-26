<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-022556** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the input expression ${{ inputs.venv }} is placed directly inside the 'Gather the metadata' run: script, in `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is pasted into the script before the shell runs it, so a crafted venv value can break out of the quotes and run its own commands. Fix: map it in the step's env block (VENV: ${{ inputs.venv }}) and refer to it as "$VENV" in the script.

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

I moved `inputs.venv` into the env block of the 'Gather the metadata' step as `VENV`. The script now uses it as "${VENV}" in both the `-n` test and the `source` line, so the value is no longer pasted into the script. I also pinned the `pytorch/test-infra/.github/actions/get-workflow-job-id@main` step to commit 13fc79c71b9a7c86a46d898782991a6418778f0b (`# main`). That's the upstream commit this mirror was built from, and I checked with lookup_action_sha that it exists. Nothing has been run or tested.

