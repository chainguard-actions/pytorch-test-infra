<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261021-234439** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action step pulls in another action by a branch name, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs.

Locations:

- `action.yml:91`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes values built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV with no sanitization step. The script reads RUNNER_TEMP but does not set it. The writes are `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`, plus the same pattern for RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR. Each of these values is "${RUNNER_TEMP}/...". The check requires `printf '%s' ... | tr -d '\n\r'` right before each write when the value comes from something other than a literal computed in the same run block.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia to commit 4bb924e6cddf98370d0c754d6769b492fe457233 (# main). This is the same upstream test-infra commit this mirror version was built from, so the nested action matches what upstream shipped. Did not check it with lookup_action_sha. In 'Setup useful environment variables', each value now goes through printf '%s' | tr -d '\n\r' before it is written to $GITHUB_ENV (RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR, RUNNER_DOCS_DIR). The values written are unchanged. Not tested.

