<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-223308** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by the mutable branch `@main` instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-uv@main` and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:31`
- `action.yml:114`

### github-env-injection (severity: high)

The 'Install dependencies' step writes `echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV`. RUNNER_TEMP is a process env var that this composite action inherits, not one the same run: script sets, so under this check it counts as workflow-controlled. The value is written to GITHUB_ENV without first running it through `printf '%s' ... | tr -d '\n\r'`.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml.

1. unpinned-uses: The two `uses:` lines (setup-uv and get-workflow-job-id) pointed at `@main`. They now point at pytorch/test-infra@d50cbade0e174f113111122f50b7a814b9b4c61d with a `# v20261125-223308` comment. That is the upstream commit this mirror version was built from, and lookup_action_sha confirmed it exists.

2. github-env-injection: In the 'Install dependencies' step, the VIRTUAL_ENV path is now passed through `printf '%s' ... | tr -d '\n\r'` before it is written to `$GITHUB_ENV`, and `$GITHUB_ENV` is quoted.

One change beyond the findings: the 'Get device type' step writes DEVICE_TYPE (a value read from the device tools) to `$GITHUB_ENV`. I strip newlines from it the same way before the write. The step still fails if DEVICE_TYPE is unset, as it did upstream, because `set -u` still applies.

