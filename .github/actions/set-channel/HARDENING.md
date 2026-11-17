<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the 'Set CHANNEL for tagged pushes' step, the run block expands GITHUB_REF_NAME without quotes: `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then`. The value comes from the pushed tag name, so it is workflow-controllable. Inside [[ ]] the left-hand side is not word-split or glob-expanded, so the real risk is low. The check still requires double quotes on every such expansion. Fix: `if [[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]; then`.

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Double-quoted ${GITHUB_REF_NAME} in the [[ ]] test in the 'Set CHANNEL for tagged pushes' step of action.yml. The right-hand pattern is still unquoted, so glob matching works as before.

