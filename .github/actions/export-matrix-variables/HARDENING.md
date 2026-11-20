<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261119-192116** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the env var TARGET_OS comes from inputs.target-os, which the calling workflow controls, and it is expanded without quotes in the 'Export variables' step: `if [[ ${TARGET_OS} != "linux" ]]; then` (line 33) and `if [[ ${TARGET_OS} == 'windows' ]]; then` (line 39). Quote it as "${TARGET_OS}". Inside [[ ]] an unquoted right-hand side of == or != is also matched as a glob pattern, so quoting "linux" and 'windows' already helps there.

Locations:

- `action.yml:33`
- `action.yml:39`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${TARGET_OS} in both [[ ]] comparisons in action.yml (lines 33 and 39). The right-hand sides were already quoted literals. Inside [[ ]] this doesn't change behavior, and the input already reached the script through env:. No other changes.

