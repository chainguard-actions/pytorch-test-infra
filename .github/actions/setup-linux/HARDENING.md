<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that points at a branch instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-nvidia@main'. Anyone who can push to that branch can change the code this action runs.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The step 'Setup useful environment variables' builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var RUNNER_TEMP. It then writes them to $GITHUB_ENV (e.g. 'echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"') without first running printf '%s' ... | tr -d '\n\r'. RUNNER_TEMP is not set by this script, so under this check it counts as workflow-controlled.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia from @main to bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c, the upstream commit this version was built from. I confirmed that SHA with lookup_action_sha and kept '# main' as a comment so the origin is still clear. In the 'Setup useful environment variables' step, the three directory paths built from RUNNER_TEMP now go through printf '%s' ... | tr -d '\n\r' before they're written to $GITHUB_ENV. Each value is captured by a plain assignment, with no nested command substitution, so a failure still stops the step under errexit. Nothing else in the action changed. I haven't run the action or any tests, so these edits are unverified beyond reading the diff.

