<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261103-202628** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the 'Export variables' step, TARGET_OS comes from inputs.target-os but is expanded without double quotes: `if [[ ${TARGET_OS} != "linux" ]]; then` (line 32) and `if [[ ${TARGET_OS} == 'windows' ]]; then` (line 38). Inside [[ ]] bash does not split words, but the check requires every expansion of workflow-controlled data to be double-quoted. Fix: use "${TARGET_OS}".

Locations:

- `action.yml:32`
- `action.yml:38`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${TARGET_OS} in both [[ ]] comparisons in action.yml (lines 32 and 38). Behavior is unchanged.

