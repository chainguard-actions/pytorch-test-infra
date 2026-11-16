<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261021-234439** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR from the inherited process env var RUNNER_TEMP. Neither the script nor anything before it sets RUNNER_TEMP. Both values are written to $GITHUB_ENV without the required sanitization step (printf '%s' ... | tr -d '\n\r'): `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"` and `echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}"`. This check counts any inherited env var in a composite run block as untrusted, so the writes should strip newlines first.

Locations:

- `action.yml:64`
- `action.yml:68`

### script-injection (severity: high)

Rule (b), unquoted shell variable expansion. In the 'Setup useful environment variables' step, the inherited env var RUNNER_TEMP is expanded without quotes inside a command substitution: `RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts"`. It should be written as `cygpath "${RUNNER_TEMP}"`.

Locations:

- `action.yml:62`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In the 'Setup useful environment variables' step: RUNNER_TEMP is now quoted when passed to cygpath. Its result goes into its own variable first, so a cygpath failure still stops the step under errexit. Both values are passed through printf '%s' | tr -d '\n\r' before they are written to $GITHUB_ENV.

