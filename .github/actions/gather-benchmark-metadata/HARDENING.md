<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261119-192116** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite step references an action by branch rather than a 40-char commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a): in the 'Gather the metadata' step, the expression ${{ inputs.venv }} is placed directly inside the run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. Template substitution happens before the shell parses the script, so a crafted venv input can run arbitrary commands. Move it into env (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

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

Pinned pytorch/test-infra/.github/actions/get-workflow-job-id to upstream commit 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4 (# main), confirmed via lookup_action_sha. Moved inputs.venv into the step env as VENV and referenced it as "${VENV}" in the bash script.

