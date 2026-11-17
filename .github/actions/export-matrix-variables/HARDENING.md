<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: TARGET_OS comes from inputs.target-os and is expanded without double quotes in shell tests: `if [[ ${TARGET_OS} != "linux" ]]; then` (line 33) and `if [[ ${TARGET_OS} == 'windows' ]]; then` (line 39). Quote it as "${TARGET_OS}". The output redirection target `>> ${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}` (lines 45 and 49) is also unquoted and should be quoted too.

Locations:

- `action.yml:33`
- `action.yml:39`
- `action.yml:45`
- `action.yml:49`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${TARGET_OS} in both [[ ]] tests and quoted the redirection target "${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}". ADD_QUOTES_AROUND_VAR (empty or a single flag) now expands as ${VAR:+"$VAR"} so behavior is unchanged.

