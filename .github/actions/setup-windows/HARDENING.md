<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261021-234439** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the 'Setup useful environment variables' step, an inherited env var is expanded without quotes inside a command substitution: `RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts"`. A composite action inherits its env from the calling workflow, so treat RUNNER_TEMP as untrusted and quote it: `$(cygpath "${RUNNER_TEMP}")`.

Locations:

- `action.yml:57`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes values built from the inherited RUNNER_TEMP env var to $GITHUB_ENV without sanitizing them first: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"` and `echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}"`. Apply `printf '%s' ... | tr -d '\n\r'` to each value right before it is written.

Locations:

- `action.yml:59`
- `action.yml:63`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, github-env-injection

**Notes:**

I fixed both findings in the 'Setup useful environment variables' step of action.yml. Nothing has been run or tested.

- script-injection: RUNNER_TEMP is now quoted when passed to cygpath. The cygpath result goes into its own variable first, so a cygpath failure still stops the step, as it did before.
- github-env-injection: RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR now have newlines and carriage returns stripped (printf '%s' ... | tr -d '\n\r') just before each is written to $GITHUB_ENV.

No other steps were changed.

