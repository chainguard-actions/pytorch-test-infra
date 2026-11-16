<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20261103-202628** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): unquoted shell expansion of workflow-controlled data in the 'Set CHANNEL for tagged pushes' step: `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then`. GITHUB_REF_NAME holds the tag or branch name, which whoever pushes the ref controls. Inside [[ ]] the shell does not word-split or glob-expand it, so the real risk is low, but the check requires a double-quoted expansion: `[[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]`.

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Put double quotes around ${GITHUB_REF_NAME} in the [[ ]] test in the 'Set CHANNEL for tagged pushes' step. The quotes go on the left side only and the pattern on the right stays unquoted, so the rc-tag match works exactly as before.

