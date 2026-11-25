<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261125-022556** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: the env var TARGET_OS comes from the workflow-controlled input inputs.target-os, and the script expands it without double quotes in two places: `if [[ ${TARGET_OS} != "linux" ]]; then` (line 33) and `if [[ ${TARGET_OS} == 'windows' ]]; then` (line 39). Inside [[ ]] bash does not split the value into words, so the practical risk is low. The rule still requires quoting, so use "${TARGET_OS}".

Locations:

- `action.yml:33`
- `action.yml:39`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the two [[ ]] tests on lines 33 and 39 now quote the variable as "${TARGET_OS}". The comparisons work exactly as before. Nothing else was changed: ${ADD_QUOTES_AROUND_VAR} is still unquoted because it is a fixed flag the script sets itself, not input from the workflow, and an empty value has to drop out of the command entirely.

