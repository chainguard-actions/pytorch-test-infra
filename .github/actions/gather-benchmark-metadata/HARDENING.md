<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261027-001733** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step uses an action by branch name instead of a commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), direct expression interpolation in the 'Gather the metadata' run block. Offending lines: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The input is placed into the script by template substitution before the shell parses it, so a crafted value can inject commands. Move it into an env var (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in double quotes.

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

I fixed all four findings in hardened/action/action.yml.

1. Unpinned action: the step used pytorch/test-infra/.github/actions/get-workflow-job-id@main. It is now pinned to 9206d491d3a5507163cb9d5b77040d4c3ef5e038, the upstream commit this release was built from. A lookup confirmed that commit exists. A trailing comment on that line records the original @main.

2. Script injection (one script-injection finding and two static-inline-injection findings, all about the same two lines): in the 'Gather the metadata' step, inputs.venv was pasted straight into the script. I added it to the step's env: block as VENV and changed the script to use "${VENV}" in double quotes, both in the empty check and in the `source` line. An empty venv still skips activation, as before.

I haven't run the action after these edits.

