<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-build-test/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-build-test/v20261103-202628** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step uses a mutable tag instead of a full 40-character commit SHA: `uses: actions/checkout@v4`. Pin it to a commit SHA, e.g. `actions/checkout@<40-hex-sha> # v4`.

Locations:

- `action.yml:36`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262 # v4 in action.yml.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In action.yml, the 'Setup useful environment variables' step now strips CR/LF from RUNNER_TEMP using printf | tr -d '\n\r' before writing RUNNER_ARTIFACT_DIR to $GITHUB_ENV.

