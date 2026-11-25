<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-232755** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references composite steps by mutable branch ref instead of a 40-char commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 122).

Locations:

- `action.yml:31`
- `action.yml:122`

### github-env-injection (severity: high)

Step 'Install dependencies' writes a value derived from the inherited process env var RUNNER_TEMP to $GITHUB_ENV without sanitization: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. The script reads RUNNER_TEMP but never sets it, so this check treats it as workflow-controlled. It needs the printf '%s' ... | tr -d '\n\r' step before the write, and $GITHUB_ENV should be quoted.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned both pytorch/test-infra sub-action references (setup-uv, get-workflow-job-id) from @main to the upstream commit 2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f (checked with lookup_action_sha) and added the comment '# v20261109-232755'. In 'Install dependencies', the VIRTUAL_ENV value now has newlines stripped with printf '%s' | tr -d '\n\r' before it is written, and "$GITHUB_ENV" is quoted. I also quoted $GITHUB_ENV in the two other writes (DEVICE_NAME, DEVICE_TYPE), which the finding did not flag. Nothing was run to test these changes.

