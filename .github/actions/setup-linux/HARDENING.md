<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261125-022556** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that uses a branch ref instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs.

Locations:

- `action.yml:93`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds values from the inherited process env var RUNNER_TEMP, which this script reads but does not set, so the calling workflow controls it. It writes them to $GITHUB_ENV without first running `printf '%s' ... | tr -d '\n\r'`. Example: `RUNNER_ARTIFACT_DIR="${RUNNER_TEMP}/artifacts"` followed by `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR are written the same way.

Locations:

- `action.yml:67`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia from @main to upstream commit 13fc79c71b9a7c86a46d898782991a6418778f0b (confirmed with lookup_action_sha; it is the commit this release was built from). In the 'Setup useful environment variables' step, RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now have newlines and carriage returns stripped with printf '%s' | tr -d '\n\r' before they are written to $GITHUB_ENV. The directory create and clean-up commands are unchanged. Nothing was tested or run, and I didn't change anything beyond these two findings.

