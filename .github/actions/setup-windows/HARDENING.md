<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261123-205410** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation in the 'Setup useful environment variables' step. The inherited env var RUNNER_TEMP is expanded without quotes inside a command substitution: `RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts"`. The outer quotes do not cover the inner expansion, so the value is split on whitespace and glob-expanded. A composite action inherits its env from the calling workflow, so treat this value as workflow-controlled. Fix: `$(cygpath "${RUNNER_TEMP}")`.

Locations:

- `action.yml:57`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes values built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV without the required sanitization (`printf '%s' ... | tr -d '\n\r'`). The writes are `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"` and `echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}"`. Both values come from RUNNER_TEMP, which the script did not set itself.

Locations:

- `action.yml:59`
- `action.yml:63`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, github-env-injection

**Notes:**

Quoted RUNNER_TEMP inside cygpath command substitution (captured separately so a cygpath failure still stops the step under errexit), and sanitized RUNNER_ARTIFACT_DIR / RUNNER_TEST_RESULTS_DIR with printf '%s' | tr -d '\n\r' before writing to GITHUB_ENV.

