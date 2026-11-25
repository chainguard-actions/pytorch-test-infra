<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that points at a branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs. Pin it to a commit SHA.

Locations:

- `action.yml:88`

### github-env-injection (severity: high)

The step 'Setup useful environment variables' builds values from the inherited process env var RUNNER_TEMP, which this script reads but does not set. It then writes them to $GITHUB_ENV without sanitizing first: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. The same happens for RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR. Pass each value through `printf '%s' ... | tr -d '\n\r'` before the write.

Locations:

- `action.yml:66`
- `action.yml:70`
- `action.yml:74`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia to bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c (the upstream commit this action version came from, so setup-nvidia matches the same test-infra snapshot; current main is d50cbade...). Removed newline/CR characters with printf | tr -d '\n\r' from RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR before they are written to $GITHUB_ENV. The mkdir/rm steps still use the original values, so they behave as before.

