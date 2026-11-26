<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261125-022556** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that references an action by a mutable branch, not a 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Pin it to a full commit SHA.

Locations:

- `action.yml:89`

### github-env-injection (severity: high)

The step 'Setup useful environment variables' builds values from the inherited process env var RUNNER_TEMP and writes them to $GITHUB_ENV without sanitizing them first. The script does not set RUNNER_TEMP itself, so under this check it counts as workflow-controlled. Affected writes: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`, and the same pattern for RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR. Pass each value through `printf '%s' ... | tr -d '\n\r'` right before the write.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia from @main to the upstream commit 13fc79c71b9a7c86a46d898782991a6418778f0b, the same test-infra commit this action version was built from. I checked the SHA with lookup_action_sha. In 'Setup useful environment variables', each of RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now goes through printf '%s' | tr -d '\n\r' right before it is written to GITHUB_ENV. The variable names and directory paths have not changed, and the rm and mkdir commands work as before. I didn't run anything to test the change.

