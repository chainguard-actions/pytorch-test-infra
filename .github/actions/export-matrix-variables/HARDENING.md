<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261021-234439** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation in the 'Export variables' step. TARGET_OS comes from the input `inputs.target-os` but is expanded without double quotes: `if [[ ${TARGET_OS} != "linux" ]]; then` (line 33) and `if [[ ${TARGET_OS} == 'windows' ]]; then` (line 39). Quote it as "${TARGET_OS}". In the same step, the redirect target `>> ${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}` (lines 44, 48) uses unquoted inherited env vars and should be quoted too: "${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}".

Locations:

- `action.yml:33`
- `action.yml:39`
- `action.yml:44`
- `action.yml:48`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In the 'Export variables' step of action.yml, added double quotes around ${TARGET_OS} in both [[ ]] tests and around the redirect target "${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}" in both branches. The inputs were already passed through env:. I left ADD_QUOTES_AROUND_VAR unquoted on purpose: the step sets it itself to either an empty string or a fixed flag, and an empty value must drop out of the command instead of becoming an empty argument.

