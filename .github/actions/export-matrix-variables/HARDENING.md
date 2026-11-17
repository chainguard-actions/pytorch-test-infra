<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: the env var TARGET_OS comes straight from inputs.target-os, but the script expands it without double quotes. Offending lines: `if [[ ${TARGET_OS} != "linux" ]]; then` and `if [[ ${TARGET_OS} == 'windows' ]]; then`. Inside [[ ]] the shell does not split words, but the check requires every expansion of workflow-controlled data to be double-quoted. Fix: use "${TARGET_OS}". (Unquoted ${RUNNER_TEMP} and ${GITHUB_RUN_ID} on the python output redirect lines are runner-provided values and should be quoted too, for safety.)

Locations:

- `action.yml:33`
- `action.yml:39`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, both [[ ]] checks now use "${TARGET_OS}" in double quotes. The redirect targets "${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}" are quoted too. ${ADD_QUOTES_AROUND_VAR} is now ${ADD_QUOTES_AROUND_VAR:+"$ADD_QUOTES_AROUND_VAR"}: the flag is still passed when set and dropped when empty, same as before. Nothing was run to test these edits.

