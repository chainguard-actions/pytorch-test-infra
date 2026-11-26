<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-223308** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps use actions pinned to a branch instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 120). Pin both to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:120`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP comes from the process environment this composite action inherits, and the script reads it without setting it, so under this check it counts as workflow-controlled. It goes into $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' step first. Fix: strip newlines from the value before the write and quote "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I pinned the two internal pytorch/test-infra actions (setup-uv and get-workflow-job-id) to commit d50cbade0e174f113111122f50b7a814b9b4c61d. That's the upstream commit this version was built from, and lookup_action_sha confirmed it. The comment '# main' keeps the original ref visible.

In the 'Install dependencies' step, the VIRTUAL_ENV value now has newlines and carriage returns stripped with printf '%s' | tr -d '\n\r' before it's written. "$GITHUB_ENV" is now quoted.

I also changed two writes that weren't in the findings. The DEVICE_TYPE write now gets the same newline stripping, since its value comes from tool output. The DEVICE_NAME write now quotes "$GITHUB_ENV". Both still behave as before under set -u. Nothing has been run or tested.

