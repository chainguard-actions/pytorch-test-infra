<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261109-192709** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the env var TARGET_OS comes from inputs.target-os, which the calling workflow controls, and it is expanded without double quotes in the 'Export variables' step: `if [[ ${TARGET_OS} != "linux" ]]; then` and `if [[ ${TARGET_OS} == 'windows' ]]; then`. Quote it as "${TARGET_OS}".

Locations:

- `action.yml:33`
- `action.yml:39`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Added double quotes around ${TARGET_OS} in both [[ ]] tests in action.yml (lines 33 and 39). While there, I made two small changes that keep behaviour the same. ADD_QUOTES_AROUND_VAR is now passed as ${ADD_QUOTES_AROUND_VAR:+"$ADD_QUOTES_AROUND_VAR"}, so the flag is still dropped when the variable is empty. The ${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID} redirect targets are now quoted. Nothing was run to test these changes.

