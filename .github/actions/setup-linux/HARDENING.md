<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261119-192116** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action step 'Install nvidia driver, nvidia-docker runtime, set GPU_FLAG' points to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs. Pin it to a specific commit SHA.

Locations:

- `action.yml:90`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia@main to commit 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4 (# main) in action.yml. That is the upstream_commit this release was built from, and it is in the same pytorch/test-infra repo, so the setup-nvidia version matches this setup-linux release. That was the only uses: reference in the action. Nothing was run to test the change.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In the 'Setup useful environment variables' step, newlines are now stripped from RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR with printf '%s' | tr -d '\n\r' right before each is written to $GITHUB_ENV. The directory create/delete commands and the values written are otherwise unchanged. The step runs under shell: bash, which sets pipefail, so a failure inside the pipe still stops the step.

