<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261029-163400** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses an action by a branch name instead of a commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Sub-rule (a): the 'Gather the metadata' step puts an expression straight into its run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The caller controls inputs.venv, so a crafted value can break out of the quotes and run commands. Pass it through an env: variable (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in double quotes instead.

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

I fixed all four findings in action.yml.

- **Unpinned action:** The `get-workflow-job-id` step used `@main`. It is now pinned to `@f2f972bd8f3eab11aa0094897a81879653c6f141 # v20261029-163400`. I looked up the tag v20261029-163400 in pytorch/test-infra and it points to that commit, which is also the upstream commit this version was built from.
- **Script injection (3 findings, same cause):** In the 'Gather the metadata' step, `inputs.venv` was written straight into the shell script. It is now passed in through the step's `env:` block as `VENV`, and the script uses `"${VENV}"` in double quotes for both the empty check and the `source`. The script behaves the same: an empty value still skips the `source`.

I didn't run anything to test these changes.

