<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step references an action by a branch name instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes values to $GITHUB_ENV without first running them through `printf '%s' ... | tr -d '\n\r'`. The values are RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR. Each one is built from the inherited process env var RUNNER_TEMP, which this script does not set, so the calling workflow controls it. Example: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"` (the same pattern is on lines 71 and 76). A newline in the value could inject extra environment variables.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia from @main to f2f972bd8f3eab11aa0094897a81879653c6f141. That is the upstream commit this mirror version (v20261029-163400) was built from; I checked it with lookup_action_sha. In the 'Setup useful environment variables' step, RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now go through printf '%s' | tr -d '\n\r' before being written to $GITHUB_ENV. The directory creation and cleanup are the same as before. Nothing was run to test these changes.

