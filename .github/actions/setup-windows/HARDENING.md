<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the 'Setup useful environment variables' step, the inherited env var RUNNER_TEMP is expanded without quotes inside a command substitution: `RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts"`. It should be quoted: `$(cygpath "${RUNNER_TEMP}")`.

Locations:

- `action.yml:57`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes values built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV without first running `printf '%s' ... | tr -d '\n\r'`: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"` and `echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}"`. Each value should go through that pipeline before it is written.

Locations:

- `action.yml:59`
- `action.yml:63`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, github-env-injection

**Notes:**

In the 'Setup useful environment variables' step, put quotes around ${RUNNER_TEMP} in the cygpath command substitution. RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR are now passed through printf '%s' | tr -d '\n\r' before being written to $GITHUB_ENV. The cygpath call is still a plain assignment, not nested inside the sanitizer, so if it fails the step still stops (errexit). Nothing else changed.

