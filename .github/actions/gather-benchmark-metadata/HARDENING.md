<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261125-022556** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step uses an action pinned to a branch, not a full commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. If that branch changes, the new code runs here and receives the github-token input. Pin it to a 40-character commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), direct expression interpolation. In the 'Gather the metadata' step, `${{ inputs.venv }}` is placed straight into the run script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted before the shell parses the script, so the caller can inject shell commands. Move it into an env variable (e.g. `VENV: ${{ inputs.venv }}`) and use it double-quoted as "$VENV".

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

Both findings are fixed in action.yml. I haven't run the action to test it.

- **Unpinned action:** `pytorch/test-infra/.github/actions/get-workflow-job-id@main` is now pinned to commit 13fc79c71b9a7c86a46d898782991a6418778f0b, with a trailing comment naming the old branch. That commit is the one this mirror was built from (the request's upstream_commit), and lookup_action_sha confirmed it exists in pytorch/test-infra. I used it rather than the current tip of `main` so the sub-action matches this release.
- **Script injection:** In the 'Gather the metadata' step, `inputs.venv` now goes into the step's env block as `VENV`, and the script uses it double-quoted as `"${VENV}"`. The empty-check and `source` work as before.

