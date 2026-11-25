<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261118-220128** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) is broken: the 'Gather the metadata' step puts the `inputs.venv` expression straight into the run: script, so the template text is pasted into the script before the shell parses it. Offending lines: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. A caller-supplied venv value containing quotes or shell metacharacters can run arbitrary commands. Fix: map the input to an env var, e.g. `VENV: ${{ inputs.venv }}`, and use `"$VENV"` in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

A composite step references an action by a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a commit SHA.

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

**Fixes applied:** script-injection, unpinned-uses, static-inline-injection

**Notes:**

All findings are fixed, all in action.yml. I haven't run the action to test the changes.

- **Unpinned action:** `get-workflow-job-id@main` now points to a fixed commit, the upstream commit this mirror was built from (bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c). I chose that over the current `main` (8cd319865066bf94e5be2b0180d081175095c980) so the sub-action stays at the same version as the rest of this release. The trailing comment `# main` keeps the original branch name visible.
- **Script injection (both findings):** the `venv` input is now passed to the 'Gather the metadata' step through `env: VENV`. The script tests and sources it as `"${VENV}"`, so a caller-supplied value can no longer be run as shell code. The step behaves the same as before: it sources the file only when the value is non-empty.

