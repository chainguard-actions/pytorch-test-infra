<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Setup useful environment variables' writes values built from the inherited process env var RUNNER_TEMP (not set by this script; composite actions inherit env from the calling workflow) to $GITHUB_ENV with no sanitization: echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}" and echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}". If the value contains a newline, extra environment variables can be injected. Fix: strip newlines first with safe=$(printf '%s' "$VAR" | tr -d '\n\r') and write "$safe" instead.

Locations:

- `action.yml:61`
- `action.yml:65`

### script-injection (severity: high)

Rule (b): the step 'Setup useful environment variables' expands the inherited env var RUNNER_TEMP without quotes inside command substitution: RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts". It should be quoted: "$(cygpath "${RUNNER_TEMP}")/artifacts".

Locations:

- `action.yml:59`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In action.yml, step 'Setup useful environment variables': ${RUNNER_TEMP} is now quoted inside the cygpath command substitution. Newlines and carriage returns are stripped with printf | tr -d '\n\r' before RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR are written to $GITHUB_ENV. The cygpath call is still a plain assignment, so if it fails the step stops, as it did upstream. Nothing was run to test the change.

