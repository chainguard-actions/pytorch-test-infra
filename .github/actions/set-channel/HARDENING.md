<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20261103-202628** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) is not met. In the step 'Set CHANNEL for tagged pushes', the line `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then` expands GITHUB_REF_NAME without quotes. This variable holds the tag name, which is the same value as github.ref_name and can be set by whoever pushes the tag. Bash does not split words or expand globs inside [[ ]], so the real risk is low. The check still requires every expansion of workflow-controlled data to be double-quoted. Fix: `if [[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]; then`.

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${GITHUB_REF_NAME} in the [[ ]] test in action.yml. The glob pattern on the right is still unquoted, so the RC-suffix match works as before.

