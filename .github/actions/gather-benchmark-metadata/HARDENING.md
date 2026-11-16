<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261029-163400** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step references an action by a branch instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'. If that branch changes, the code this action runs changes with it.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), direct expression interpolation: the 'Gather the metadata' step puts the ${{ inputs.venv }} expression straight into its run: script, on these lines: 'if [[ -n "${{ inputs.venv }}" ]]; then' and 'source "${{ inputs.venv }}"'. A crafted venv value can break out of the quotes and run arbitrary shell commands. Fix: pass inputs.venv through an env: variable (e.g. VENV) and use "$VENV" in the script.

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

Pinned get-workflow-job-id to f2f972bd8f3eab11aa0094897a81879653c6f141, the upstream commit this mirror version was built from (current main is c91174703a48...); the '# main' comment is kept. Moved inputs.venv into env VENV and the script now uses "${VENV}" for both the -n check and the source line.

