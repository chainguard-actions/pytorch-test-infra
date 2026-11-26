<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261125-223308** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the 'Export variables' step, the env var TARGET_OS comes straight from inputs.target-os, which the calling workflow controls. It is expanded without quotes in two places: line 33 `if [[ ${TARGET_OS} != "linux" ]]; then` and line 39 `if [[ ${TARGET_OS} == 'windows' ]]; then`. Inside [[ ]] bash does not split the value into words. But on the right of a pattern match, an unquoted value is still handled loosely, and the check requires every expansion of workflow-controlled data to be double-quoted. Fix: change both lines to "${TARGET_OS}".

Locations:

- `action.yml:33`
- `action.yml:39`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Put double quotes around ${TARGET_OS} in both [[ ]] comparisons in action.yml (lines 33 and 39). The right-hand sides are fixed strings, so these checks behave exactly as before. I left ${ADD_QUOTES_AROUND_VAR} unquoted on purpose: it only ever holds an empty string or a fixed flag the script sets itself, never workflow input. If it were quoted, its empty value would be passed to the script as an extra empty argument. Nothing was run to test the change.

