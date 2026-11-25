<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step uses a branch ref instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs.

Locations:

- `action.yml:95`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var RUNNER_TEMP. It writes them to $GITHUB_ENV without the `printf '%s' ... | tr -d '\n\r'` sanitization step, e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. RUNNER_TEMP is not set inside this run: script, so under the check's rule (e) it counts as workflow-controlled.

Locations:

- `action.yml:68`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia from @main to commit e9b5b0a4c36ebfde49dec880ae77705038009471. That is the upstream commit this mirror version was built from, and I checked the SHA with lookup_action_sha. In the 'Setup useful environment variables' step, RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now go through printf '%s' | tr -d '\n\r' before they are written to $GITHUB_ENV. The directory creation and cleanup are unchanged. Nothing was run to test these changes.

