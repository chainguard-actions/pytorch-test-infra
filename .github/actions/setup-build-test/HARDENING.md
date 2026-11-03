<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-build-test/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-build-test/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that uses a mutable tag instead of a full 40-character commit SHA: `uses: actions/checkout@v4`.

Locations:

- `action.yml:36`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes an inherited process env var to $GITHUB_ENV without cleaning it first: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_TEMP}/artifacts" >> "${GITHUB_ENV}"`. RUNNER_TEMP is not set inside this run script, so the check treats it as controlled by the calling workflow. A newline in it could inject extra environment variables. Clean it first: safe=$(printf '%s' "$RUNNER_TEMP" | tr -d '\n\r'), then write "RUNNER_ARTIFACT_DIR=${safe}/artifacts".

Locations:

- `action.yml:45`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). Stripped newlines from RUNNER_TEMP before writing RUNNER_ARTIFACT_DIR to GITHUB_ENV.

