<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-build-test/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-build-test/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action step references a mutable tag instead of a full 40-character commit SHA: `uses: actions/checkout@v4`. Fix: pin it to that tag's full commit SHA, with the tag kept as a trailing comment.

Locations:

- `action.yml:36`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned actions/checkout@v4 to its full commit SHA, 11d5960a326750d5838078e36cf38b85af677262, and kept '# v4' as a trailing comment. This was the only change in action.yml and nothing was run to test it.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

Sanitized RUNNER_TEMP-derived value with printf | tr -d '\n\r' before writing RUNNER_ARTIFACT_DIR to $GITHUB_ENV in action.yml.

