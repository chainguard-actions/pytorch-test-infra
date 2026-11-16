<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Two composite action steps point to a mutable branch ref instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115). Pin both to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is an inherited process env var that this run script does not set. In a composite action the calling workflow controls inherited env, so this check treats it as untrusted. The value is written to $GITHUB_ENV without the required sanitization step (printf '%s' ... | tr -d '\n\r'). Fix: compute safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'), then write "VIRTUAL_ENV=$safe" to "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned setup-uv and get-workflow-job-id to the upstream commit f2f972bd8f3eab11aa0094897a81879653c6f141 (# main), the commit this mirror version was built from. In the Install dependencies step, the VIRTUAL_ENV value now goes through printf '%s' | tr -d '\n\r' before it is written to the quoted "$GITHUB_ENV".

