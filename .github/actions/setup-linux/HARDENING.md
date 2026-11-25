<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite action step points to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs. Pin it to a commit SHA.

Locations:

- `action.yml:88`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var RUNNER_TEMP. This script does not set RUNNER_TEMP, so under this check it counts as workflow-controlled. The step then writes those values to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`) with no `printf '%s' ... | tr -d '\n\r'` sanitization first. A newline in the value could inject extra environment variables.

Locations:

- `action.yml:63`
- `action.yml:68`
- `action.yml:73`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in action.yml.

- **unpinned-uses:** The `setup-nvidia` step used the `main` branch. It is now pinned to upstream commit bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c, which is the commit this mirror version (v20261118-220128) was built from. I checked the SHA with `lookup_action_sha`. A trailing comment records where it came from.
- **github-env-injection:** In the 'Setup useful environment variables' step, `RUNNER_TEMP` and each directory value now go through `printf '%s' ... | tr -d '\n\r'` before anything is written to `$GITHUB_ENV`. For a normal `RUNNER_TEMP` with no newlines, the three directory paths and the commands that create them come out exactly as before.

I haven't run the action after these changes.

