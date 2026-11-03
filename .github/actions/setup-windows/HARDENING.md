<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Setup useful environment variables' writes RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR to $GITHUB_ENV. Both values are built from the process env var RUNNER_TEMP, which the composite action inherits and does not compute itself. Neither value goes through the required sanitisation (printf '%s' ... | tr -d '\n\r') before the write. Offending lines: echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}" and echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}". The runner normally sets RUNNER_TEMP, but the check counts every inherited env var as untrusted.

Locations:

- `action.yml:59`
- `action.yml:63`

### script-injection (severity: high)

Sub-rule (b) is violated: an inherited env var is expanded without quotes in step 'Setup useful environment variables'. Offending line: RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts". The ${RUNNER_TEMP} inside the command substitution should be written as "${RUNNER_TEMP}".

Locations:

- `action.yml:57`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection

**Notes:**

Quoted ${RUNNER_TEMP} inside the cygpath command substitution. RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR are now sanitized with printf '%s' | tr -d '\n\r' before being written to $GITHUB_ENV. Command substitution of cygpath kept as a bare assignment so errexit behavior is unchanged.

