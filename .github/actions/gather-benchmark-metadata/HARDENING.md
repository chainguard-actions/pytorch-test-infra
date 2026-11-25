<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261119-192116** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step points to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), direct expression interpolation. The 'Gather the metadata' run block puts `${{ inputs.venv }}` straight into the shell script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. Move inputs.venv into an env: variable (e.g. VENV) and use it as "$VENV".

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

Both findings are fixed in action.yml. I haven't run the action to test the changes.

1. Pinned action: the `get-workflow-job-id` step pointed at the `main` branch. It now points at commit 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4, with a `# main` comment so the original ref is still visible. That commit is the upstream commit this version of the action was built from, and I looked it up to confirm it exists in pytorch/test-infra. A later change to `main` could make that step behave differently from upstream's.

2. Script injection: the 'Gather the metadata' step used to paste `inputs.venv` straight into the script. It is now passed in through a `VENV` environment variable on that step, and the script uses it as "${VENV}" in both the empty check and the `source` line. Behaviour is the same as before.

