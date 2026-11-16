<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20260922-155642** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Setup useful environment variables' writes values built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV without the `printf '%s' ... | tr -d '\n\r'` sanitization: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"` and `echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}"`. In a composite action, a calling workflow can set RUNNER_TEMP, and the script reads it rather than computing it, so this check treats it as untrusted. Fix: strip newlines first, e.g. `safe=$(printf '%s' "$RUNNER_ARTIFACT_DIR" | tr -d '\n\r')`, then write `$safe`.

Locations:

- `action.yml:59`
- `action.yml:63`

### script-injection (severity: high)

Rule (b): unquoted expansion of workflow-controllable env data in step 'Setup useful environment variables': `RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts"`. The ${RUNNER_TEMP} inside the command substitution is not double-quoted. Fix: `$(cygpath "${RUNNER_TEMP}")`.

Locations:

- `action.yml:57`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In the 'Setup useful environment variables' step: quoted ${RUNNER_TEMP} in the cygpath call, and sanitized both RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR with printf '%s' | tr -d '\n\r' before writing them to $GITHUB_ENV. No other behavior changed.

