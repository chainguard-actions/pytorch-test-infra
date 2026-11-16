<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261103-202628** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): an expression is placed directly inside the 'Gather the metadata' run: script. The lines are `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The caller controls inputs.venv, and the value is pasted into the script before the shell runs it, so a crafted value can break out of the quotes and run commands. Fix: add `VENV: ${{ inputs.venv }}` to the step's env: block and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

A uses: reference points to a branch, not a commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a full 40-character commit SHA.

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

I moved `inputs.venv` into the env: block of the 'Gather the metadata' step as `VENV`. The script now uses "${VENV}" for both the empty check and the `source` line, and the step still sources the venv only when the input is set. I pinned `pytorch/test-infra/.github/actions/get-workflow-job-id@main` to e9b5b0a4c36ebfde49dec880ae77705038009471, the upstream commit this mirror version was built from, with a `# main` comment. I didn't use the commit main points to now (a0cd49277f4b12dc98a9a6af1e23332c21aa7a00) so the sub-action matches the rest of this release. Nothing was run to test the change.

