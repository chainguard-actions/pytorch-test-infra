<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261112-155209** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Setup useful environment variables' writes values built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV without sanitizing them first. The script reads RUNNER_TEMP but never sets it, so under this check it counts as workflow-controlled. The two writes are: echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}" and echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}". Neither is preceded by printf '%s' ... | tr -d '\n\r'.

Locations:

- `action.yml:61`

### script-injection (severity: high)

Rule (b): in step 'Setup useful environment variables', an env var is expanded without quotes inside a command substitution: RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts". The script inherits ${RUNNER_TEMP} from the environment and does not quote it. Use "$(cygpath "${RUNNER_TEMP}")/artifacts" instead.

Locations:

- `action.yml:59`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In action.yml, step 'Setup useful environment variables': quoted ${RUNNER_TEMP} inside the cygpath command substitution, and removed CR/LF from RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR (printf '%s' | tr -d '\n\r') before writing them to $GITHUB_ENV. The step's commands, the directories it creates and the variable names are unchanged.

