<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261123-205410** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: the env var TARGET_OS comes from inputs.target-os, which the calling workflow controls, and the script expands it without quotes: `if [[ ${TARGET_OS} != "linux" ]]; then` (line 33) and `if [[ ${TARGET_OS} == 'windows' ]]; then` (line 39). Quote it as "${TARGET_OS}". In the same step, the redirect targets `>> ${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}` (lines 44 and 48) expand the inherited env vars RUNNER_TEMP and GITHUB_RUN_ID without quotes. They should be quoted as well: "${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}".

Locations:

- `action.yml:33`
- `action.yml:39`
- `action.yml:44`
- `action.yml:48`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml I put double quotes around ${TARGET_OS} in both [[ ]] tests. I also quoted both redirect targets as "${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}". One change goes beyond the finding: ${ADD_QUOTES_AROUND_VAR} is now ${ADD_QUOTES_AROUND_VAR:+"$ADD_QUOTES_AROUND_VAR"}, so the flag stays quoted when set and drops out when empty, which matches what upstream did. I checked the final file by reading it back, but I haven't run the action.

