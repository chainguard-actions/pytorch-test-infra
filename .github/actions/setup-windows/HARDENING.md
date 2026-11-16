<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261109-192709** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Setup useful environment variables' writes values built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV without sanitizing them first: echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}" and echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}". A composite action inherits its env from the calling workflow, so the value is not computed inside this script. Pass each value through printf '%s' ... | tr -d '\n\r' before writing it.

Locations:

- `action.yml:59`

### script-injection (severity: high)

Rule (b): an inherited env var is expanded without quotes inside command substitution in step 'Setup useful environment variables': RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts". Quote it as "$(cygpath "${RUNNER_TEMP}")/artifacts".

Locations:

- `action.yml:57`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In action.yml, 'Setup useful environment variables' step: quoted ${RUNNER_TEMP} inside the cygpath command substitution, and sanitized RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR with printf '%s' | tr -d '\n\r' before writing them to $GITHUB_ENV. cygpath failure still aborts the step as before (the assignment itself is unchanged apart from quoting).

