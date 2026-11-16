<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20260922-155642** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action step pins its action to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Anyone who can push to that branch changes the code this action runs.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), direct expression interpolation: in the 'Gather the metadata' step, the run block puts `${{ inputs.venv }}` straight into the shell script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted before bash parses the script, so a crafted venv input can break out of the quotes and run arbitrary commands. Fix: move it into an env var (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

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

I pinned the get-workflow-job-id action to a commit instead of the main branch. I used 28dee7456d0348d74a5faa85098bb028b263ee2b, the upstream commit this mirror was built from, so the sub-action matches the rest of the code. The line keeps a '# main' comment. The current tip of main is c91174703a487849783425932bef8cdf24e3154c, which is newer. I also moved inputs.venv into the step's env: block as VENV and changed the script to use "${VENV}" in both the -n check and the source line. I did not run anything to test these changes.

