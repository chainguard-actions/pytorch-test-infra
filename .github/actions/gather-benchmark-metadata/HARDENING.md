<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261118-220128** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step points to a branch, not a commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Whoever controls that branch can change the code this action runs. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), direct expression interpolation: the 'Gather the metadata' step puts `${{ inputs.venv }}` straight into the run script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The input is pasted into the script before the shell runs, so a crafted value can inject commands. Pass it through an env variable (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

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

Both findings are fixed in action.yml. I haven't run the action to test the changes.

- **Unpinned action:** `get-workflow-job-id@main` now points to the full commit `bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c`, with a `# main` comment. That's the upstream commit this version was built from, not the current tip of `main` (that tip is `058f82ec7cd2fb6cbe66f44cccd28a8c8861b072`). I chose it so the sub-action matches the rest of this release.
- **Script injection:** in the 'Gather the metadata' step, `inputs.venv` is now passed through the step's `env:` block as `VENV`. The script reads it as a quoted `"${VENV}"` in both the `-n` check and the `source` line, and does the same thing as before.

