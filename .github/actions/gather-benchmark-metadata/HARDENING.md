<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261109-232755** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a), direct expression interpolation: in the 'Gather the metadata' step, the run: block puts `${{ inputs.venv }}` straight into the shell script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script before the shell runs it, so a crafted input can inject commands. Fix: pass the input through an env: variable (e.g. `VENV: ${{ inputs.venv }}`) and reference it as "$VENV" in double quotes.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

A composite step points at a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

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

I moved inputs.venv into a VENV env var on the 'Gather the metadata' step. The script now uses "${VENV}" in double quotes, both in the -n test and in the source line. I also pinned pytorch/test-infra/.github/actions/get-workflow-job-id to commit 2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f (# main). That is the upstream commit this mirror version was built from, so the sub-action runs the same code it had when the version was built, not whatever main points to now. lookup_action_sha confirmed the commit exists. Nothing has been run or re-scanned since the change.

