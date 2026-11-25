<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261109-192709** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step refers to its action by a branch, not a commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:91`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var RUNNER_TEMP. This script does not set RUNNER_TEMP, so the check treats it as workflow-controlled. Each value is written to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`) with no `printf '%s' ... | tr -d '\n\r'` step before the write.

Locations:

- `action.yml:66`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml. Nothing was run or tested.

1. unpinned-uses: the setup-nvidia step pointed at the `main` branch. It is now pinned to commit 0569df511711f70601c984fe3a93dac324afc9ce, the upstream commit this mirror version was built from, so it matches the rest of the action. I took that SHA from the request rather than resolving the current tip of `main`, which may have moved since then.

2. github-env-injection: the 'Setup useful environment variables' step now strips newline and carriage-return characters from RUNNER_TEMP once, into SAFE_RUNNER_TEMP. RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR are built from that cleaned value before being written to $GITHUB_ENV. The paths come out the same as before. The capture uses a plain assignment and a pipeline, and the composite bash shell has pipefail on, so a failure is not hidden.

