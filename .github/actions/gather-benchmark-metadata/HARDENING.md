<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261118-220128** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step uses a branch ref instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Sub-rule (a): the 'Gather the metadata' step puts a GitHub Actions expression directly inside its run: script. The offending lines are `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. Because the input is substituted into the script before bash runs it, a crafted venv value can run arbitrary shell commands. Fix: add `VENV: ${{ inputs.venv }}` to the step's env: block and use "$VENV" in the script.

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

- **Unpinned sub-action:** `get-workflow-job-id` was referenced as `@main`. It is now pinned to `bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c # main`. That is the upstream test-infra commit this action version was built from, so the sub-action matches it. It is not the current tip of `main`. I confirmed the SHA exists with lookup_action_sha.
- **Script injection:** `inputs.venv` was pasted straight into the 'Gather the metadata' script. It now goes through the step's env as `VENV`, and the script uses `"${VENV}"` in both the empty check and the `source` line. The behaviour is unchanged: an empty value still skips the `source`.

