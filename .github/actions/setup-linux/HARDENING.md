<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step pins its action to a branch instead of a commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this step runs. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:90`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia@main to 9206d491d3a5507163cb9d5b77040d4c3ef5e038, the upstream test-infra commit this setup-linux release (v20261027-001733) was built from. Both actions now run from the same commit.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In the 'Setup useful environment variables' step of action.yml, each of RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now has newlines and carriage returns stripped (printf '%s' | tr -d '\n\r') just before it is written to $GITHUB_ENV. Directory creation and cleanup work as before. I haven't run the action to test the change.

