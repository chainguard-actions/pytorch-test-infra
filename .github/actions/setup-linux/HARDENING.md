<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action step 'Install nvidia driver, nvidia-docker runtime, set GPU_FLAG' points at a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Pin it to a specific commit SHA, with the branch or tag name in a comment.

Locations:

- `action.yml:90`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia@main to 6f7274a0eff04dd4f8ada574e4e144610cece2c8 (# main), the upstream commit for v20261112-155209. This matches the sub-action to the same commit this action version was built from, so it does not track the current main HEAD (a1a8f075...).

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In the 'Setup useful environment variables' step, RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR are now sanitized with printf '%s' ... | tr -d '\n\r' immediately before being written to $GITHUB_ENV. Directory creation/removal logic unchanged.

