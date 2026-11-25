<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261125-022556** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action step pins its action to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs.

Locations:

- `action.yml:86`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds values from the inherited process env var RUNNER_TEMP, which this run script does not set. It writes them to $GITHUB_ENV without first running `printf '%s' ... | tr -d '\n\r'`, e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. The same applies to RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR. The runner normally sets RUNNER_TEMP, but the check treats any inherited env var as untrusted, so these writes need the sanitization step.

Locations:

- `action.yml:64`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia@main to commit 13fc79c71b9a7c86a46d898782991a6418778f0b, the upstream commit this mirror version was built from. I checked the SHA with lookup_action_sha. The 'Setup useful environment variables' step now strips newlines from RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR with printf '%s' ... | tr -d '\n\r' before writing them to GITHUB_ENV. Nothing was run to test the changes. Nothing else changed.

