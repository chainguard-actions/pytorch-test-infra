<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-windows/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-windows/v20261109-232755** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Setup useful environment variables' builds RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR from the inherited RUNNER_TEMP variable, which the script reads but does not set. It then writes both values to $GITHUB_ENV without running them through printf '%s' ... | tr -d '\n\r' first: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"` and `echo "RUNNER_TEST_RESULTS_DIR=${RUNNER_TEST_RESULTS_DIR}" >> "${GITHUB_ENV}"`. Strip newlines from each value before writing it.

Locations:

- `action.yml:59`
- `action.yml:63`

### script-injection (severity: high)

Rule (b), unquoted variable expansion: step 'Setup useful environment variables' expands the inherited env var RUNNER_TEMP without quotes inside a command substitution: `RUNNER_ARTIFACT_DIR="$(cygpath ${RUNNER_TEMP})/artifacts"`. Change it to `cygpath "${RUNNER_TEMP}"`.

Locations:

- `action.yml:57`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In action.yml's 'Setup useful environment variables' step: quoted ${RUNNER_TEMP} in the cygpath command substitution, and passed both RUNNER_ARTIFACT_DIR and RUNNER_TEST_RESULTS_DIR through printf '%s' | tr -d '\n\r' before writing to $GITHUB_ENV. The cygpath assignment stays a bare assignment so errexit behavior is unchanged.

