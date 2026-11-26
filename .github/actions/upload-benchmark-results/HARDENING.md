<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite steps in action.yml use branch refs where they should use full commit SHAs: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:120`

### github-env-injection (severity: high)

The 'Install dependencies' step writes a value built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' sanitization step: echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV. The check treats any env var the script reads but did not set itself as untrusted. Fix: safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'); echo "VIRTUAL_ENV=$safe" >> "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned the setup-uv and get-workflow-job-id sub-actions from @main to commit 13fc79c71b9a7c86a46d898782991a6418778f0b. That is the upstream commit this version was built from, and lookup_action_sha confirmed it exists. Each pin keeps a '# main' comment. In the 'Install dependencies' step, the VIRTUAL_ENV value now goes through printf '%s' ... | tr -d '\n\r' before it is written to the quoted "$GITHUB_ENV". Nothing was run to test these edits.

