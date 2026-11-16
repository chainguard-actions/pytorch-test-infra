<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261029-163400** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): TARGET_OS holds the workflow-controlled input inputs.target-os (set via env:), but it is expanded without quotes in the 'Export variables' step: `if [[ ${TARGET_OS} != "linux" ]]; then` (line 33) and `if [[ ${TARGET_OS} == 'windows' ]]; then` (line 39). Both should use "${TARGET_OS}".

Locations:

- `action.yml:33`
- `action.yml:39`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${TARGET_OS} in both [[ ]] comparisons in the 'Export variables' step of action.yml. The input was already passed via env:, and the comparison results stay the same.

