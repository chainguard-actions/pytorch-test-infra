<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20261119-192116** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b), unquoted expansion of workflow-controlled data. In the 'Set CHANNEL for tagged pushes' step, the line `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then` expands GITHUB_REF_NAME without quotes. Its value is the pushed tag name, which whoever pushes the tag controls. Inside [[ ]] the left side is not word-split or glob-expanded, so the real-world risk is low. The check still requires double quotes. Fix: `if [[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]; then` and leave the pattern on the right unquoted so it still matches as a glob.

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${GITHUB_REF_NAME} in the [[ ]] test in action.yml; the glob pattern on the right is still unquoted so it keeps matching -rc suffixes.

