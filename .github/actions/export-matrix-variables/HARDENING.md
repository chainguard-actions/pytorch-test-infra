<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the input-derived env var TARGET_OS (from inputs.target-os) is expanded without quotes in the 'Export variables' step: `if [[ ${TARGET_OS} != "linux" ]]; then` and `if [[ ${TARGET_OS} == 'windows' ]]; then`. Bash does not split words inside [[ ]], but the check requires every expansion of workflow-controlled data to be double-quoted, so these should be "${TARGET_OS}". The output redirection targets `>> ${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}` (lines 44 and 48) are also unquoted and should be quoted to be safe.

Locations:

- `action.yml:32`
- `action.yml:38`
- `action.yml:44`
- `action.yml:48`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${TARGET_OS} in both [[ ]] tests and quoted the >> "${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}" redirect targets. Changed the optional flag ${ADD_QUOTES_AROUND_VAR} to ${ADD_QUOTES_AROUND_VAR:+"$ADD_QUOTES_AROUND_VAR"} so it is still left out when empty.

