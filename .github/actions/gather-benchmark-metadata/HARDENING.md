<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261029-163400** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml pins a composite step to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Sub-rule (a): the 'Gather the metadata' step puts an expression directly into its run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The input value is pasted into the shell script before it runs, so a crafted value can execute commands. Pass it through an env variable (e.g. VENV: ${{ inputs.venv }}) and reference it as "$VENV".

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

I made two fixes in hardened/action/action.yml.

1. Unpinned action: the `get-workflow-job-id` step now uses commit f2f972bd8f3eab11aa0094897a81879653c6f141 instead of the `main` branch, with `# main` kept as a comment. This is the upstream commit this version was built from, and I confirmed it exists in pytorch/test-infra. It is not the current tip of `main`.

2. Script injection: in the 'Gather the metadata' step, `inputs.venv` is now passed in through `env:` as `VENV`. The script checks and sources it as "${VENV}" instead of pasting the input into the script. The step behaves the same as before: it only sources the venv when the input isn't empty.

I haven't run the action or any tests after these edits.

