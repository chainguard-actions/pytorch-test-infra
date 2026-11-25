<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Gather the metadata' step puts the expression inputs.venv straight into the run script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. GitHub fills in the value before bash runs, so the quotes don't protect it and a crafted value can run shell commands. Fix: add VENV: ${{ inputs.venv }} to the step's env: block and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

Unpinned action reference: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main` points to a branch that can change. Pin it to a full 40-character commit SHA.

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

All findings are fixed in action.yml. Not tested: I made no test runs.

1. **Script injection (venv input):** The 'Gather the metadata' step no longer pastes `inputs.venv` straight into the script. The input now goes into the step's `env:` block as `VENV`, and the script reads it as "${VENV}".

2. **Unpinned action:** `pytorch/test-infra/.github/actions/get-workflow-job-id@main` is now pinned to `6f7274a0eff04dd4f8ada574e4e144610cece2c8 # main`. I took that SHA from the request's upstream_commit field. I did not look it up with lookup_action_sha. It is the test-infra commit this mirror version was built from. That makes it the same `get-workflow-job-id` code upstream ran at this version, though not necessarily the latest commit on `main`.

