<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261125-223308** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step references an action by a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code that runs in this action. Pin it to a commit SHA.

Locations:

- `action.yml:91`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var RUNNER_TEMP. It then writes them to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`) without first running `printf '%s' ... | tr -d '\n\r'`. Under this check, any env var a composite action inherits counts as workflow-controlled, so these values must be sanitized before the write.

Locations:

- `action.yml:63`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in action.yml.

- **unpinned-uses:** The nested `pytorch/test-infra/.github/actions/setup-nvidia@main` step now points at upstream_commit d50cbade0e174f113111122f50b7a814b9b4c61d, with a `# v20261125-223308 (was main)` comment. That commit is the test-infra commit this mirror version was built from, so the nested action now runs at the same commit as the rest of the action. I took it from the request rather than looking it up with `lookup_action_sha`, which would have given the current tip of `main` instead.
- **github-env-injection:** In the 'Setup useful environment variables' step, `RUNNER_TEMP` now has newlines and carriage returns stripped (`printf '%s' | tr -d '\n\r'`) before it is used to build the directory paths. Each of `RUNNER_ARTIFACT_DIR`, `RUNNER_TEST_RESULTS_DIR` and `RUNNER_DOCS_DIR` is stripped again right before it is written to `$GITHUB_ENV`.

Nothing was run or tested. On a normal runner `RUNNER_TEMP` contains no newlines, so the values the step writes should be the same as before.

