<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Setup useful environment variables' writes values built from the inherited process env var RUNNER_TEMP (not set by this script, and a calling workflow can override it) to $GITHUB_ENV without the sanitization step printf '%s' ... | tr -d '\n\r'. The lines are: echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}" and echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}".

Locations:

- `action.yml:59`
- `action.yml:63`

### script-injection (severity: high)

Rule (b): in step 'Setup useful environment variables', the inherited env var RUNNER_TEMP is expanded without quotes inside command substitution: RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts". Quote it as "${RUNNER_TEMP}".

Locations:

- `action.yml:57`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In action.yml step 'Setup useful environment variables': quoted ${RUNNER_TEMP} in the cygpath call (captured as its own assignment so errexit still applies), and sanitized RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR via printf '%s' | tr -d '\n\r' before writing to $GITHUB_ENV. Behavior otherwise unchanged.

