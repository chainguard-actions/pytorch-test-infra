<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the step 'Set CHANNEL for tagged pushes', the run: block expands GITHUB_REF_NAME without double quotes: `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then`. The value is the tag or branch name, and whoever pushes the ref chooses it. Bash's [[ ]] does not word-split or glob-expand the left side, so the real risk is small. The check still requires every expansion of workflow-controlled data to be double-quoted. Fix: `[[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]`. Leave the right-hand pattern unquoted so it still works as a glob.

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Put double quotes around ${GITHUB_REF_NAME} in the [[ ]] test in the 'Set CHANNEL for tagged pushes' step of action.yml. I left the right-hand pattern *-rc[0-9]* unquoted, so it still matches as a glob and behaviour doesn't change. No other files were changed, and nothing was run to test the edit.

