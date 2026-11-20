<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261119-192116** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Gather the metadata' step puts the ${{ inputs.venv }} expression straight into the run: script, on lines `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script text before bash runs, so a crafted venv input can inject shell commands. Fix: map it through env (VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

A composite step refers to an action by branch instead of commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a full 40-character commit SHA.

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

Both fixes are in action.yml.

1. Script injection (script-injection and static-inline-injection, lines 57-58): the 'Gather the metadata' step pasted the venv input straight into its script. It now passes the input in through the step's env: block as VENV, and the script reads "${VENV}" in the empty check and in the source line. Behaviour is unchanged.

2. Unpinned action (unpinned-uses, line 38): the get-workflow-job-id step now points at commit 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4 instead of the main branch, with a '# main' comment for readability. That is the upstream commit this mirror version was built from, taken from the request; I did not check it separately with a lookup. Current main resolves to a newer commit, 8a253c90..., but pinning to the build commit keeps the sub-action matching the rest of this version.

