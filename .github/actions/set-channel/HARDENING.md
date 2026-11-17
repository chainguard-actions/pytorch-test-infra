<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b), unquoted variable expansion, in step 'Set CHANNEL for tagged pushes'. The line is `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then`. GITHUB_REF_NAME holds the pushed tag name, and whoever pushes the tag chooses it, yet it is expanded without double quotes. Bash's [[ ]] does not word-split or glob-expand the left-hand operand, so the practical risk is low. The check still requires every expansion of workflow-controllable data to be quoted. Fix: `if [[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]; then`, leaving the right-hand pattern unquoted so it still matches as a glob.

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Added double quotes around ${GITHUB_REF_NAME} in the [[ ]] test in the 'Set CHANNEL for tagged pushes' step. The right-hand pattern is still unquoted, so it is still matched as a glob.

