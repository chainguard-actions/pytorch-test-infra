<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261123-205410** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step references an action by a branch name instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Whoever controls that branch can change the code this action runs.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), direct expression interpolation: the 'Gather the metadata' step puts the `inputs.venv` expression straight into the run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The caller controls this value, and it is substituted into the script before the shell parses it, so it can inject shell commands. Fix: pass it in through an env: variable (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

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

Both findings are fixed in action.yml. I haven't run the action since the edit.

- **Unpinned `uses:`:** `get-workflow-job-id` now points at commit 8c9ea89f444b15c5ce4bb833a0cfed044a2667f7, with `# main` kept as a comment. I didn't look up the current head of `main`. I pinned to the upstream commit this version was built from, and checked that it resolves. That keeps the sub-action at the same code as the rest of this release.
- **Script injection:** in the 'Gather the metadata' step, the `inputs.venv` value now comes in through `VENV:` under `env:`. The script reads it as `"${VENV}"` in both places (the empty check and the `source` line).

