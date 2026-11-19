<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the 'Setup useful environment variables' step, the inherited env var RUNNER_TEMP is expanded without quotes inside a command substitution: `RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts"`. The outer double quotes do not cover the inner expansion inside $(...), so the shell splits the value on whitespace and expands globs. This is a composite action, so env vars come from the calling workflow and count as workflow-controlled. Fix: `$(cygpath "${RUNNER_TEMP}")`.

Locations:

- `action.yml:57`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes values built from the inherited env var RUNNER_TEMP to $GITHUB_ENV without stripping newlines first: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"` and `echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}"`. Both values come from RUNNER_TEMP, which the script reads but does not set. Fix: clean each value with `safe=$(printf '%s' "$VAR" | tr -d '\n\r')` right before the write.

Locations:

- `action.yml:59`
- `action.yml:63`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, github-env-injection

**Notes:**

Quoted ${RUNNER_TEMP} inside the cygpath command substitution; newline/CR-stripped RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR via printf|tr before writing to $GITHUB_ENV (shell: bash, composite runs with pipefail).

