<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20260922-155642** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Setup useful environment variables' builds RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR from the inherited process env var RUNNER_TEMP. It then writes both to $GITHUB_ENV without first running printf '%s' ... | tr -d '\n\r' on them: echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}" and echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}". RUNNER_TEMP is not set inside this script, and a composite action inherits its env from the calling workflow, so this check treats it as untrusted.

Locations:

- `action.yml:64`

### script-injection (severity: high)

Rule (b) violation in step 'Setup useful environment variables': the inherited env var RUNNER_TEMP is expanded without quotes inside a command substitution: RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts". It should be written as "$(cygpath "${RUNNER_TEMP}")/artifacts".

Locations:

- `action.yml:62`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In action.yml, step 'Setup useful environment variables': ${RUNNER_TEMP} is now double-quoted inside the cygpath command substitution. RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR now have newlines removed with printf '%s' | tr -d '\n\r' before they are written to $GITHUB_ENV. Each tr runs on an already-assigned variable rather than wrapping a command, so if cygpath fails the step still stops (errexit). The unused working-directory: ${{ inputs.repository }} was left as upstream wrote it. Not run or tested.

