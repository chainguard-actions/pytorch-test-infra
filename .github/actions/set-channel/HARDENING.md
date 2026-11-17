<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) unquoted shell variable expansion: the step 'Set CHANNEL for tagged pushes' expands ${GITHUB_REF_NAME} without double quotes: `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then`. GITHUB_REF_NAME is the tag or branch name, which whoever pushes the tag or branch controls. Inside [[ ]] the left side is not word-split or glob-expanded, so the real-world risk is low. Still, the check requires every expansion of workflow-controllable data to be double-quoted. Fix: `if [[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]; then` (keep the pattern on the right side unquoted so it still works as a glob).

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${GITHUB_REF_NAME} in the [[ ]] test in action.yml; glob pattern on right side left unquoted.

