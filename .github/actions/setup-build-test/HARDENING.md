<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-build-test/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-build-test/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses a mutable tag instead of a full 40-character commit SHA: `uses: actions/checkout@v4`.

Locations:

- `action.yml:37`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes `echo "RUNNER_ARTIFACT_DIR=${RUNNER_TEMP}/artifacts" >> "${GITHUB_ENV}"`. RUNNER_TEMP comes in from the process environment; this script does not set it. The value is written to GITHUB_ENV without first being cleaned with `printf '%s' "$RUNNER_TEMP" | tr -d '\n\r'`. A composite action inherits its environment from the calling workflow, so this check treats the value as untrusted.

Locations:

- `action.yml:46`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (# v4). RUNNER_TEMP now has newlines and carriage returns stripped (printf | tr -d '\n\r') before it is written to GITHUB_ENV.

