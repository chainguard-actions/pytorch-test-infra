<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the env var TARGET_OS comes from inputs.target-os and is expanded without double quotes in the 'Export variables' step: `if [[ ${TARGET_OS} != "linux" ]]; then` and `if [[ ${TARGET_OS} == 'windows' ]]; then`. Inside [[ ]] it is the left operand, so it is not word-split, but it is still an unquoted expansion of workflow-controlled data. Fix: write "${TARGET_OS}".

Locations:

- `action.yml:32`
- `action.yml:38`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Added double quotes around ${TARGET_OS} in both [[ ]] tests in action.yml (lines 32 and 38). The input was already passed in through env:, and the script's behavior is unchanged.

