<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261109-192709** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: the env var TARGET_OS comes from inputs.target-os, which the calling workflow controls, but it is expanded without double quotes in the 'Export variables' step: `if [[ ${TARGET_OS} != "linux" ]]; then` and `if [[ ${TARGET_OS} == 'windows' ]]; then`. Quote it as "${TARGET_OS}".

Locations:

- `action.yml:33`
- `action.yml:39`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In the 'Export variables' step of action.yml, both `[[ ... ]]` comparisons now quote ${TARGET_OS}. The step behaves exactly as before. I also quoted the redirect target path built from RUNNER_TEMP and GITHUB_RUN_ID; this was not part of the finding and is only an extra precaution. I left ${ADD_QUOTES_AROUND_VAR} unquoted on purpose: the script sets it itself to either an empty string or one fixed flag, so no outside input reaches it. Quoting it would hand the Python script an empty argument whenever it is empty. Nothing was run or tested after the edits.

