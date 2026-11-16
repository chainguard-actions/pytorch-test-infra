<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step points to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), direct expression interpolation: the 'Gather the metadata' step puts `${{ inputs.venv }}` straight into its run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The caller controls this input, and its value is substituted into the script before the shell parses it. Pass it through an env var instead (e.g. VENV: ${{ inputs.venv }}) and use it double-quoted as "$VENV".

Locations:

- `action.yml:56`
- `action.yml:57`

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

I pinned pytorch/test-infra/.github/actions/get-workflow-job-id to commit 6f7274a0eff04dd4f8ada574e4e144610cece2c8 and kept '# main' as a comment. That commit is the upstream_commit this mirror version was built from, so the sub-action stays at the same version as the rest of the action. The current main is c91174703a487849783425932bef8cdf24e3154c and was not used. I moved inputs.venv into the step's env: block as VENV. The script now reads it double-quoted as "${VENV}" in both the -n test and the source command. No tests were run.

