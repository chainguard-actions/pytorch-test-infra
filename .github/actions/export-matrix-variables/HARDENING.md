<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: the env var TARGET_OS comes straight from inputs.target-os, so the calling workflow controls it, and it is expanded without double quotes in the 'Export variables' step. Offending lines: `if [[ ${TARGET_OS} != "linux" ]]; then` and `if [[ ${TARGET_OS} == 'windows' ]]; then`. Fix: quote both, e.g. `[[ "${TARGET_OS}" != "linux" ]]` and `[[ "${TARGET_OS}" == 'windows' ]]`.

Locations:

- `action.yml:33`
- `action.yml:39`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${TARGET_OS} in both [[ ]] tests in the 'Export variables' step of action.yml. Behavior is unchanged: inside [[ ]] the left side is never word-split, and the right-hand patterns were already literal quoted strings. The input was already passed through env:.

