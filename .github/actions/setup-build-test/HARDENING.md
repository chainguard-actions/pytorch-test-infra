<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-build-test/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-build-test/v20261109-232755** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite step uses a mutable tag instead of a full 40-character commit SHA: `uses: actions/checkout@v4`.

Locations:

- `action.yml:37`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes `RUNNER_ARTIFACT_DIR=${RUNNER_TEMP}/artifacts` to $GITHUB_ENV. RUNNER_TEMP is a process env var that the composite action inherits and does not set in its own script. The value is not passed through `printf '%s' ... | tr -d '\n\r'` before the write. Strip newlines first, e.g. `safe=$(printf '%s' "$RUNNER_TEMP" | tr -d '\n\r'); echo "RUNNER_ARTIFACT_DIR=${safe}/artifacts" >> "$GITHUB_ENV"`.

Locations:

- `action.yml:46`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262 (# v4). RUNNER_TEMP now has newlines stripped (printf | tr -d '\n\r') before RUNNER_ARTIFACT_DIR is written to GITHUB_ENV.

