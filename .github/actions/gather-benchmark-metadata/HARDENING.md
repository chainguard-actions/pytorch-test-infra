<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261103-202628** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml refers to an action by a branch name instead of a commit SHA: 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a): the 'Gather the metadata' step puts an expression straight into its run: script. The lines are 'if [[ -n "${{ inputs.venv }}" ]]; then' and 'source "${{ inputs.venv }}"'. The value is substituted into the script before the shell runs, so a crafted input can inject commands. Pass it through an env: variable (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

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

I made two changes to action.yml.

1. Pinned the action reference. `pytorch/test-infra/.github/actions/get-workflow-job-id` was pointing at the `main` branch. It now points at commit e9b5b0a4c36ebfde49dec880ae77705038009471 (with a `# main` comment). That is the upstream commit this release was built from, so the job-id action runs at the same code as this release. I took the SHA from the request and did not look it up separately.

2. Removed the injection risk in the 'Gather the metadata' step. The `inputs.venv` value no longer goes straight into the script: it is passed in through a `VENV` environment variable, and the script reads it as "${VENV}" in both the `-n` check and the `source` line. The step behaves the same as before.

