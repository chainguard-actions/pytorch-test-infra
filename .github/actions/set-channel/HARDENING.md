<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: an unquoted shell expansion of workflow-controlled data in the 'Set CHANNEL for tagged pushes' step. The line is `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then`. GITHUB_REF_NAME holds the tag or branch name, which whoever pushes the ref can choose. Inside [[ ]] bash does not split words or expand globs on the left side, so this is low risk in practice. The check still requires the expansion to be double-quoted. Fix: `if [[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]; then`.

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${GITHUB_REF_NAME} in the [[ ]] test in action.yml. The right side is still an unquoted glob, so the match works the same as before.

