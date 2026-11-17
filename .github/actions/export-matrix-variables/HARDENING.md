<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261021-234439** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the composite step 'Export variables', the env var TARGET_OS (set from inputs.target-os) is expanded without double quotes: line 33 `if [[ ${TARGET_OS} != "linux" ]]; then` and line 39 `if [[ ${TARGET_OS} == 'windows' ]]; then`. Bash does not word-split inside [[ ]], so the real risk is low. The check still requires every expansion of workflow-controlled data to be double-quoted. Change both to "${TARGET_OS}".

Locations:

- `action.yml:33`
- `action.yml:39`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Added double quotes around both ${TARGET_OS} expansions in the [[ ]] tests in action.yml (lines 33 and 39). The comparisons work the same as before. ADD_QUOTES_AROUND_VAR is still unquoted, as upstream had it: it is a fixed value set by the script and may be empty, and leaving it unquoted means no empty argument is passed when it is empty.

