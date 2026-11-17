<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20261109-192709** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the step 'Set CHANNEL for tagged pushes' expands GITHUB_REF_NAME without quotes: `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then`. The value comes from the pushed tag name, which whoever pushes the tag controls. Inside [[ ]] the shell does not split or glob the left-hand side, so the practical risk is low. The check still requires every expansion of workflow-controlled data to be double-quoted. Fix: `[[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]` (keep the pattern on the right unquoted so it still matches as a glob).

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${GITHUB_REF_NAME} in the [[ ]] test in action.yml; RC glob pattern left unquoted so matching behavior is unchanged.

