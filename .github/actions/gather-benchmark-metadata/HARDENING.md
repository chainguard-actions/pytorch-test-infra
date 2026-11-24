<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261123-205410** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that points to a branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), direct expression interpolation: the 'Gather the metadata' run block puts `${{ inputs.venv }}` straight into the shell script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script text before the shell runs, so a crafted input can inject commands. Fix: pass the input through an env var (for example `VENV: ${{ inputs.venv }}`) and use "$VENV" in quotes.

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

I fixed all four findings in action.yml. I haven't run the action to test the changes.

- **Unpinned action:** `pytorch/test-infra/.github/actions/get-workflow-job-id@main` now points at commit `8c9ea89f444b15c5ce4bb833a0cfed044a2667f7`, with a `# main` comment kept for readability. That is the upstream commit this version was built from. I confirmed the commit exists with lookup_action_sha.
- **Script injection (one script-injection finding and both static-inline-injection findings):** `inputs.venv` now goes into the step's `env:` block as `VENV`. The script uses `"${VENV}"` in quotes in both the empty check and the `source` line, so the input can no longer be run as shell code.

