<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261029-163400** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: the env var TARGET_OS comes from inputs.target-os, which the calling workflow controls, and it is expanded without double quotes in shell tests: `if [[ ${TARGET_OS} != "linux" ]]; then` and `if [[ ${TARGET_OS} == 'windows' ]]; then`. Quote it as "${TARGET_OS}". Inside [[ ]] the unquoted left-hand side is not word-split, but the check requires every expansion of workflow-controlled data to be double-quoted. The same applies to the unquoted ${RUNNER_TEMP} in the output redirect target, which a composite action inherits from the calling environment.

Locations:

- `action.yml:33`
- `action.yml:39`
- `action.yml:44`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, I put double quotes around ${TARGET_OS} in both [[ ]] tests. I also quoted the ${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID} redirect targets in both branches. ${ADD_QUOTES_AROUND_VAR} is now written ${ADD_QUOTES_AROUND_VAR:+"$ADD_QUOTES_AROUND_VAR"}, so it is quoted when set and passes no argument when empty, the same as before. Nothing else changed in how the action behaves. Not tested; the changes are only reviewed by reading.

