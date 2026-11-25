<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261029-163400** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step uses a branch ref instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Whoever controls that branch can change the code this action runs. Pin it to a commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Sub-rule (a), direct expression interpolation. The 'Gather the metadata' step puts `${{ inputs.venv }}` straight into its run script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The expression is substituted before the shell parses the script, so a crafted venv value can break out of the quotes and run arbitrary commands. Fix: map the input to an env var (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

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

Both findings are fixed in action.yml.

- **Unpinned `uses:`:** `pytorch/test-infra/.github/actions/get-workflow-job-id@main` is now pinned to commit f2f972bd8f3eab11aa0094897a81879653c6f141. That is the upstream commit this mirror version (v20261029-163400) was built from, so it is not today's tip of `main`. I confirmed the commit exists with lookup_action_sha.
- **Script injection:** `inputs.venv` is now passed in through a `VENV` env var on the 'Gather the metadata' step, and the script reads `"${VENV}"` instead of the inline `${{ inputs.venv }}` expression. Nothing else in the step changed.

I haven't run the action after these edits.

