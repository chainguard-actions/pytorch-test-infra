<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261123-205410** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references an action by a mutable branch instead of a full commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a) violation in the 'Gather the metadata' step: the expression `${{ inputs.venv }}` is placed directly inside the run: script, at `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script before the shell parses it, so a crafted input can run arbitrary commands. Fix: add `VENV: ${{ inputs.venv }}` to the step's env: block and use "$VENV" in the script.

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

Pinned the get-workflow-job-id action to the upstream commit 8c9ea89f444b15c5ce4bb833a0cfed044a2667f7, which lookup_action_sha confirmed exists. This is the commit this version was built from, used in place of the moving main branch. In the 'Gather the metadata' step, moved inputs.venv into the step's env: block as VENV, and the script now uses "${VENV}" in both the -n check and the source line. Not tested at runtime.

