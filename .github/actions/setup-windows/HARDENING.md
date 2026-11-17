<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Setup useful environment variables' writes values built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV with no sanitization: echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}" and echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}". The script reads RUNNER_TEMP but never sets it, so under this check it counts as workflow-controlled. Fix: run each value through printf '%s' "$VAR" | tr -d '\n\r' right before writing it.

Locations:

- `action.yml:59`
- `action.yml:63`

### script-injection (severity: high)

Rule (b), unquoted variable expansion: in step 'Setup useful environment variables' the line RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts" expands the inherited env var RUNNER_TEMP without quotes inside a command substitution. Fix: use "$(cygpath "${RUNNER_TEMP}")/artifacts".

Locations:

- `action.yml:57`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In the 'Setup useful environment variables' step: quoted RUNNER_TEMP inside the cygpath command substitution, and passed RUNNER_ARTIFACT_DIR / RUNNER_TEST_RESULTS_DIR through printf '%s' | tr -d '\n\r' before writing them to $GITHUB_ENV. Nothing else changed.

