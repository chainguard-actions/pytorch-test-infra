<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-022556** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Gather the metadata' step puts the expression ${{ inputs.venv }} straight into the run: script, in `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script text before the shell runs, so a crafted value can break out of the quotes and run its own commands. Fix: set it through env (VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

A composite step pins an action to a branch instead of a full commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Anyone who can push to that branch changes the code this action runs.

Locations:

- `action.yml:38`

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

**Fixes applied:** script-injection, static-inline-injection, unpinned-uses

**Notes:**

I fixed all three findings in action.yml.

- **Script injection (`script-injection` and both `static-inline-injection` locations):** the 'Gather the metadata' step no longer puts `inputs.venv` straight into the script. It is now set as `VENV: ${{ inputs.venv }}` in the step's `env:` block, and the script uses `"${VENV}"` in the `-n` check and the `source` call.
- **Unpinned `uses:` (`unpinned-uses`):** the `pytorch/test-infra/.github/actions/get-workflow-job-id` step was pinned to the `main` branch. It is now pinned to commit 13fc79c71b9a7c86a46d898782991a6418778f0b, with a `# main` comment.

About the pin: I didn't look up where `main` currently points. That commit is the upstream commit this mirror version was built from, given as upstream_commit in the request. The sub-action comes from the same repository, so pinning it there keeps it matched to the rest of this action. Newer changes on upstream's `main` won't be picked up.

Nothing was run or tested after the changes.

