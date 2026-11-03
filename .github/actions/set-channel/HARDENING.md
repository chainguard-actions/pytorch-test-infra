<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--set-channel/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--set-channel/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (b): the first step ('Set CHANNEL for tagged pushes') expands an env var holding workflow-controllable data without double quotes. The offending line is `if [[ ${GITHUB_REF_NAME} = *-rc[0-9]* ]]; then`. GITHUB_REF_NAME comes from github.ref_name, which is the pushed tag name. Bash does not word-split or glob the left side of [[ ]], so actual exploitation is unlikely. The check still requires a double-quoted expansion, e.g. `[[ "${GITHUB_REF_NAME}" = *-rc[0-9]* ]]`; leave the right-hand pattern unquoted so the glob still matches.

Locations:

- `action.yml:15`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Quoted ${GITHUB_REF_NAME} on the left side of the [[ ]] test in the 'Set CHANNEL for tagged pushes' step. The right-hand pattern *-rc[0-9]* is still unquoted so it keeps working as a glob.

