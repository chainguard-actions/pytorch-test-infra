<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261118-220128** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b), unquoted expansion of workflow-controlled data. TARGET_OS comes from inputs.target-os, and the script expands it without double quotes in two conditionals: `if [[ ${TARGET_OS} != "linux" ]]; then` (line 33) and `if [[ ${TARGET_OS} == 'windows' ]]; then` (line 39). Quote it as "${TARGET_OS}".

Locations:

- `action.yml:33`
- `action.yml:39`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Added double quotes around ${TARGET_OS} in both [[ ]] checks in action.yml (lines 33 and 39). Inside [[ ]] bash doesn't word-split or glob the left side, so the action behaves exactly as before. The input was already passed through env:, so no ${{ }} expression appears in the run: script. I left ${ADD_QUOTES_AROUND_VAR} unquoted on purpose. It is set inside the script, not taken from the workflow, and is either empty or a single flag. Quoting it would pass an empty argument to the Python script on Linux. Nothing was run to test this change.

