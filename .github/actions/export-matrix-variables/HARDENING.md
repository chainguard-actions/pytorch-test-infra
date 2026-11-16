<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--export-matrix-variables/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--export-matrix-variables/v20261103-202628** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the env var TARGET_OS comes from inputs.target-os, but the run: block expands it without double quotes: `if [[ ${TARGET_OS} != "linux" ]]; then` and `if [[ ${TARGET_OS} == 'windows' ]]; then`. Quote it as "${TARGET_OS}". The same script also leaves the inherited env path `${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}` unquoted in its output redirections. Quote those as well.

Locations:

- `action.yml:33`
- `action.yml:40`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml I added double quotes around ${TARGET_OS} in both [[ ]] tests. I also quoted both output redirect paths, which now read >> "${RUNNER_TEMP}/github_env_${GITHUB_RUN_ID}". One change goes beyond the finding: the optional --add-quotes-around-value flag is now passed as ${ADD_QUOTES_AROUND_VAR:+"$ADD_QUOTES_AROUND_VAR"}. It stays quoted when set and is left out entirely when empty, as before. Nothing has been run or tested yet.

