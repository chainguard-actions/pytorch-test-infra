<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in step 'Set CHANNEL for tagged pushes', the run block expands the ref name without quotes: `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then`. Whoever pushes a tag controls GITHUB_REF_NAME. Bash does not split words or expand globs on the left side of [[ ]], so the real risk here is low. The check still requires every expansion of workflow-controlled data to be double-quoted, the same way it treats case words. Fix: `if [[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]; then`. Leave the right-hand pattern unquoted so it still works as a glob.

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Double-quoted ${GITHUB_REF_NAME} on the left side of the [[ ]] test in action.yml. The right-hand glob pattern is still unquoted, so it keeps working as a pattern.

