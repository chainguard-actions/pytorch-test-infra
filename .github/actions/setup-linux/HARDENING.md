<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action step pins to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds values from the inherited process env var RUNNER_TEMP, which this run: script does not set. It writes them to $GITHUB_ENV with no `printf '%s' ... | tr -d '\n\r'` sanitization first. The three writes are: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`, `echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}"` and `echo "RUNNER_DOCS_DIR=${RUNNER_DOCS_DIR}" >> "${GITHUB_ENV}"`. Sanitize each value right before it is written.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml.

1. unpinned-uses: The `setup-nvidia` step pointed at `main`, which can change at any time. It is now pinned to `pytorch/test-infra/.github/actions/setup-nvidia@bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c`. I used the upstream commit this mirror version was built from rather than the current tip of `main`, so the step runs the same code upstream shipped in v20261118-220128. lookup_action_sha confirmed the commit exists in pytorch/test-infra.

2. github-env-injection: In the 'Setup useful environment variables' step, `RUNNER_ARTIFACT_DIR`, `RUNNER_TEST_RESULTS_DIR` and `RUNNER_DOCS_DIR` are each now passed through `printf '%s' ... | tr -d '\n\r'` right before being written to `$GITHUB_ENV`. The `mkdir` and `rm` lines above them are unchanged. Nothing was run to test the edits.

