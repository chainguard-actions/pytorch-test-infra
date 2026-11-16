<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-build-test/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-build-test/v20261109-192709** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite step points to a mutable tag instead of a full 40-character commit SHA: `uses: actions/checkout@v4`. Pin it to a commit SHA, e.g. `actions/checkout@<sha> # v4`.

Locations:

- `action.yml:37`

### github-env-injection (severity: high)

The step 'Setup useful environment variables' writes `echo "RUNNER_ARTIFACT_DIR=${RUNNER_TEMP}/artifacts" >> "${GITHUB_ENV}"`. RUNNER_TEMP is an inherited process env var, not one this run: script sets itself, so under the composite-action rule it counts as workflow-controlled. It goes into $GITHUB_ENV without the required `printf '%s' "$RUNNER_TEMP" | tr -d '\n\r'` step first. Fix: put the sanitized value in a variable and write that variable instead.

Locations:

- `action.yml:45`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262 (kept '# v4' comment). Before writing RUNNER_ARTIFACT_DIR to GITHUB_ENV, RUNNER_TEMP now has newline and carriage-return characters stripped with printf | tr -d '\n\r'.

