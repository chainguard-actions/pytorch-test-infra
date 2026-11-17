<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-build-test/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-build-test/v20260922-155642** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step in action.yml refers to an action by a version tag instead of a full 40-character commit SHA: `uses: actions/checkout@v4`. Whoever controls the tag can move it to different code. Pin it to a commit SHA and keep the version as a comment, e.g. `actions/checkout@<sha> # v4`.

Locations:

- `action.yml:36`

### github-env-injection (severity: high)

The step 'Setup useful environment variables' writes an inherited process env var to $GITHUB_ENV without sanitizing it first: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_TEMP}/artifacts" >> "${GITHUB_ENV}"`. RUNNER_TEMP is normally set by the runner, but it is not computed in this script. A composite action inherits env from the workflow that calls it, so the check treats the value as untrusted. To fix it, strip newlines first: `safe=$(printf '%s' "${RUNNER_TEMP}/artifacts" | tr -d '\n\r')`, then write `RUNNER_ARTIFACT_DIR=$safe`.

Locations:

- `action.yml:44`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (# v4). Strip newlines from ${RUNNER_TEMP}/artifacts before writing RUNNER_ARTIFACT_DIR to $GITHUB_ENV.

