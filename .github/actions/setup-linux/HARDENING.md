<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step refers to an action by branch instead of by a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Because `main` can change at any time, whatever is pushed there will run with this action's privileges. Pin it to a commit SHA.

Locations:

- `action.yml:92`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia from @main to the full commit SHA 9206d491d3a5507163cb9d5b77040d4c3ef5e038. That is the upstream commit this version of setup-linux was built from, and both actions live in the same repo. I didn't call lookup_action_sha because it resolves tags or branches, and resolving main would return whatever main points to today. The commit is the one given in the request's upstream_commit. Nothing else in action.yml was changed.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In the 'Setup useful environment variables' step, RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now go through printf '%s' | tr -d '\n\r' before being written to $GITHUB_ENV. The directories are still created and cleaned up as before.

