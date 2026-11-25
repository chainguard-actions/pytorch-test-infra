<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite steps reference actions by a mutable branch ref instead of a 40-char commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

Step 'Install dependencies' writes a value derived from an inherited process env var (RUNNER_TEMP, not computed in the same run block) to $GITHUB_ENV without the sanitization step: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. Apply safe=$(printf '%s' "$VIRTUAL_ENV" | tr -d '\n\r') before writing, and quote "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned the two pytorch/test-infra sub-actions (setup-uv, get-workflow-job-id) to 6f7274a0eff04dd4f8ada574e4e144610cece2c8, the upstream commit this version was built from. I took that SHA from the request and did not look up what main points to now. Each pin keeps a '# main' comment. In action.yml, the writes of VIRTUAL_ENV, DEVICE_NAME and DEVICE_TYPE to $GITHUB_ENV now strip newlines with printf | tr -d '\n\r', and $GITHUB_ENV is quoted. Only VIRTUAL_ENV was in the findings; I gave the other two the same treatment. The script's existing set -eux behaviour is unchanged. I haven't run the action to test these changes.

