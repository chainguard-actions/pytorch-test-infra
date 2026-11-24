<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261123-205410** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action step uses a branch ref instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs. Pin it to a full commit SHA.

Locations:

- `action.yml:90`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia@main to commit 8c9ea89f444b15c5ce4bb833a0cfed044a2667f7, the upstream commit this mirror version was built from (lookup_action_sha confirmed it exists). That way setup-nvidia comes from the same commit as setup-linux, and the line keeps '# main' as a comment.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In the 'Setup useful environment variables' step, each value built from RUNNER_TEMP (RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR, RUNNER_DOCS_DIR) now has newline and carriage-return characters stripped with printf '%s' ... | tr -d '\n\r' before it is written to $GITHUB_ENV. The steps that create and clean up the directories are unchanged. Nothing was run to test the change.

