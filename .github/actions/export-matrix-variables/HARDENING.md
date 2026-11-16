<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the 'Export variables' step expands the workflow-controlled env var TARGET_OS (from ${{ inputs.target-os }}) without double quotes: `if [[ ${TARGET_OS} != "linux" ]]; then` and `if [[ ${TARGET_OS} == 'windows' ]]; then`. Write it as "${TARGET_OS}".

Locations:

- `action.yml:32`
- `action.yml:38`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted the ${TARGET_OS} expansions in both [[ ]] tests in action.yml (lines 32 and 38). The value was already passed in through env:, so no other changes were needed. ${ADD_QUOTES_AROUND_VAR} stays unquoted on purpose: the script sets it to a fixed value or leaves it empty, so it drops out as an argument when empty.

