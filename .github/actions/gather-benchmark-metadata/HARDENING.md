<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-022556** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that points to a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a full commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), direct expression interpolation: the 'Gather the metadata' run block puts `${{ inputs.venv }}` straight into the shell script, in `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted before the shell parses the line, so a crafted input can run arbitrary commands. Move it into an env var (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

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

Pinned pytorch/test-infra/.github/actions/get-workflow-job-id to the upstream commit 13fc79c71b9a7c86a46d898782991a6418778f0b (the same upstream commit this action was built from, from the request's upstream_commit), with '# main' comment. Moved inputs.venv into the step's env: as VENV and referenced it as "${VENV}" in the 'Gather the metadata' run script.

