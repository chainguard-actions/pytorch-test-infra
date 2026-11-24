<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20261123-205410** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: an unquoted shell variable expands a ref name that whoever pushes the tag controls. Offending line: `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then`. Inside [[ ]] the left side is not word-split or glob-expanded, so the real risk is low. The check still requires the expansion to be double-quoted. Fix: `if [[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]; then`. This keeps the right-hand side as a pattern, so the behaviour does not change.

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Double-quoted ${GITHUB_REF_NAME} on the left-hand side of the [[ ]] test in action.yml. The right-hand side stays an unquoted pattern, so behaviour is unchanged.

