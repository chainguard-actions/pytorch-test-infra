<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-build-test/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-build-test/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that points to a version tag instead of a full 40-character commit SHA: `uses: actions/checkout@v4`. A tag can be moved to different code, so this is a supply-chain risk. Fix: pin it to a commit SHA and keep the tag as a comment, e.g. `actions/checkout@<40-hex-sha> # v4`.

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

In action.yml, the 'Setup useful environment variables' step now strips newline and carriage-return characters from RUNNER_TEMP before writing RUNNER_ARTIFACT_DIR to $GITHUB_ENV. When RUNNER_TEMP has no newlines (the normal case, since the runner sets it), the step writes exactly the same value as before. Nothing was run to test the change.

