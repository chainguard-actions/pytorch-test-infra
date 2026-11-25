<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references an action by a mutable branch instead of a full commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Sub-rule (a): the 'Gather the metadata' step puts the expression ${{ inputs.venv }} straight into its run: script. The offending lines are `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. GitHub substitutes the value into the script text before bash runs, so a crafted venv value can break out of the quotes and run its own commands. Fix: map it in env (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

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

I made two changes to action.yml. Nothing was run or tested.

1. Pinned the get-workflow-job-id sub-action. It was `@main`; it is now pinned to `6f7274a0eff04dd4f8ada574e4e144610cece2c8 # main`. That is the upstream commit this mirror version was built from, so the sub-action matches the rest of the action. I did not use the current tip of main (058f82ec7cd2fb6cbe66f44cccd28a8c8861b072), because that would pull in sub-action code newer than the version being mirrored.

2. Fixed the script injection in the 'Gather the metadata' step. The venv input is now passed through the step's env as `VENV`, and the script uses `"${VENV}"` in both the `-n` test and the `source` line. The script no longer contains the input text, so a crafted value can't run its own commands. It still goes to `source` as before.

