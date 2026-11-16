<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the step 'Set CHANNEL for tagged pushes' expands an untrusted variable without quotes: `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then`. GITHUB_REF_NAME is the tag name, and whoever pushes the tag chooses it. Inside [[ ]] bash does not split words or expand globs on the left side, so this is hard to exploit. It still breaks the rule that every expansion of workflow-controllable data must be double-quoted. Fix: write it as `[[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]` and leave the pattern on the right unquoted.

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${GITHUB_REF_NAME} on the left side of the [[ ]] test in the 'Set CHANNEL for tagged pushes' step. The glob pattern on the right is still unquoted, so the RC match works the same as before.

