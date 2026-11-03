<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (b): env var TARGET_OS (from ${{ inputs.target-os }}) is expanded without double quotes in the 'Export variables' step: `if [[ ${TARGET_OS} != "linux" ]]; then` and `if [[ ${TARGET_OS} == 'windows' ]]; then`. Quote it as "${TARGET_OS}". Also quote ${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID} in the redirections.

Locations:

- `action.yml:32`
- `action.yml:38`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Put double quotes around ${TARGET_OS} in both [[ ]] tests, and around the ${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID} redirect targets. Changed ADD_QUOTES_AROUND_VAR to ${ADD_QUOTES_AROUND_VAR:+"$ADD_QUOTES_AROUND_VAR"} so it is still quoted when set, and when empty on linux it still adds no argument.

