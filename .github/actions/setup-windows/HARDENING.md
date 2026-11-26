<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261125-223308** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the 'Setup useful environment variables' step expands the inherited env var RUNNER_TEMP without quotes inside a command substitution: `RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts"`. This is a composite action, so it inherits its environment from the calling workflow, and the check says to treat such variables as workflow-controlled. Quote the variable: `$(cygpath "${RUNNER_TEMP}")`.

Locations:

- `action.yml:58`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR from the inherited env var RUNNER_TEMP. The script does not set RUNNER_TEMP, so under this check it counts as workflow-controlled. Both values are written to $GITHUB_ENV with no sanitization step (`printf '%s' ... | tr -d '\n\r'`) first: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"` and `echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}"`. If the value contains a newline, extra environment variables can be injected.

Locations:

- `action.yml:60`
- `action.yml:64`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, github-env-injection

**Notes:**

Quoted RUNNER_TEMP in the cygpath command substitution. Newlines are now stripped from RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR with printf | tr -d '\n\r' before they are written to GITHUB_ENV. The mkdir steps still use the original values, as upstream does. A cygpath failure still stops the step under errexit, because the sanitize happens in a separate assignment.

