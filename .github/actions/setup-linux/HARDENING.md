<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261125-223308** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step whose `uses:` points at a branch, not a full commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this step runs at any time. Pin it to a 40-character commit SHA.

Locations:

- `action.yml:86`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes values built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV with no `printf '%s' ... | tr -d '\n\r'` sanitization first. The writes are `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`, and the same for RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR. Each value is "${RUNNER_TEMP}/...". This is a composite action and the script does not set RUNNER_TEMP itself, so under this check it counts as workflow-controlled. A newline in it could add extra environment variables. Strip newlines from each value before writing it.

Locations:

- `action.yml:63`
- `action.yml:68`
- `action.yml:73`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned the setup-nvidia step to d50cbade0e174f113111122f50b7a814b9b4c61d with a '# main' comment. This is the upstream commit this release was built from, and I confirmed the SHA with lookup_action_sha. In the 'Setup useful environment variables' step, the RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR values now go through printf '%s' | tr -d '\n\r' before they are written to $GITHUB_ENV. The written values stay the same. Nothing has been run or re-scanned to test these changes.

