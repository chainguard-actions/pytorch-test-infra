<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261109-192709** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references a composite step by branch, not by a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a) is violated in the 'Gather the metadata' step: the run: block puts the expression `${{ inputs.venv }}` straight into the shell script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script text before the shell runs, so a crafted input can inject commands. Pass it through an env: variable (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in double quotes.

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

Pinned pytorch/test-infra/.github/actions/get-workflow-job-id to commit 0569df511711f70601c984fe3a93dac324afc9ce (the upstream commit, checked with lookup_action_sha; the '# main' comment keeps the original branch name). Moved inputs.venv into an env var VENV in the 'Gather the metadata' step. The script now uses "${VENV}" in double quotes for both the -n test and the source call.

