<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): TARGET_OS comes from the workflow-controlled input `inputs.target-os` and is expanded without double quotes: `if [[ ${TARGET_OS} != "linux" ]]; then` (line 34) and `if [[ ${TARGET_OS} == 'windows' ]]; then` (line 40). Quote it as "${TARGET_OS}".

Locations:

- `action.yml:34`
- `action.yml:40`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Put double quotes around ${TARGET_OS} in both [[ ]] checks in action.yml (lines 34 and 40). The input was already passed in through env:, so this is all the finding needed. The comparisons still work exactly as before. I didn't run the action after the change. I left ${ADD_QUOTES_AROUND_VAR} unquoted on purpose: the script sets it itself, and it has to disappear when it's empty.

