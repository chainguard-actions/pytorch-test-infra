<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261109-232755** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Setup useful environment variables' builds values from the inherited process env var RUNNER_TEMP: RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts" and RUNNER_TEST_RESULTS_DIR="${RUNNER_TEMP}/test-results". It then writes them to $GITHUB_ENV with echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}" and echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}". Neither value goes through printf '%s' ... | tr -d '\n\r' first. A composite action inherits its environment from the calling workflow, so this check treats the value as workflow-controlled. If it contained a newline, it could inject extra environment variables.

Locations:

- `action.yml:64`

### script-injection (severity: high)

Rule (b): an env var is expanded without quotes in step 'Setup useful environment variables': RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts". Inside the command substitution, ${RUNNER_TEMP} is unquoted, so the shell splits it on whitespace and expands glob characters. It should be "$(cygpath "${RUNNER_TEMP}")/artifacts".

Locations:

- `action.yml:63`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In the 'Setup useful environment variables' step of action.yml: put quotes around ${RUNNER_TEMP} inside the cygpath command, and passed RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR through printf '%s' | tr -d '\n\r' before writing them to $GITHUB_ENV. The directories are still created from the original paths. Nothing was run or tested.

