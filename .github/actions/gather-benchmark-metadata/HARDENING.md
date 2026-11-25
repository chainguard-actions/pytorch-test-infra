<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261027-001733** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that refers to an action by a branch name instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Anyone who can push to that branch can change what code this action runs.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Sub-rule (a): the expression `${{ inputs.venv }}` is written directly into the 'Gather the metadata' run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is pasted into the script before bash parses it, so a crafted input can inject shell commands. Fix: pass it through env (e.g. `VENV: ${{ inputs.venv }}`) and use `"$VENV"` in the script.

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

I fixed all findings in hardened/action/action.yml. Nothing was run or tested.

- unpinned-uses: the get-workflow-job-id step was pinned to `@main`. It is now pinned to the upstream commit this mirror was built from, 9206d491d3a5507163cb9d5b77040d4c3ef5e038, with a `# main` comment. Current main is a different commit (8cd31986...). I chose the build commit so the sub-action stays at the same version as the rest of this action.
- script-injection / static-inline-injection: `inputs.venv` was pasted straight into the 'Gather the metadata' script. It now goes through the step's env as `VENV` and the script uses `"${VENV}"`, so behaviour is unchanged.

Not changed: the script runs `${GITHUB_ACTION_PATH}/../../scripts/benchmarks/gather_metadata.py`, which only works if the mirror keeps upstream's folder layout. I didn't confirm that it does.

