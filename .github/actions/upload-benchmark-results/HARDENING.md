<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose `uses:` refs point to a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-uv@main` and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes `echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV`. RUNNER_TEMP comes from the process environment this composite action inherits; the script does not set it. It is written to GITHUB_ENV without first running it through `printf '%s' ... | tr -d '\n\r'`, which the check requires for inherited env vars. Sanitize the value first and quote "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned the two pytorch/test-infra sub-actions (setup-uv, get-workflow-job-id) to upstream_commit f2f972bd8f3eab11aa0094897a81879653c6f141 (the commit this mirror version was built from, confirmed with lookup_action_sha), with a '# main' comment. In 'Install dependencies', the VIRTUAL_ENV value is now passed through printf | tr -d '\n\r' before it is written, and $GITHUB_ENV is quoted.

