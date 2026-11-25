<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Two composite action steps point to a mutable branch instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115). Pin each one to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step runs 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP comes from the process environment and is not set inside this run: script. A composite action inherits its environment from the calling workflow, so under this check RUNNER_TEMP counts as workflow-controlled. It is written to $GITHUB_ENV without the required sanitization (printf '%s' ... | tr -d '\n\r'). Strip CR/LF from the value first, and quote "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned both pytorch/test-infra sub-actions (setup-uv, get-workflow-job-id) from @main to commit 6f7274a0eff04dd4f8ada574e4e144610cece2c8, the upstream commit this version was built from, so the sub-actions match the release. The commit SHA was checked with lookup_action_sha. In the 'Install dependencies' step, CR/LF are now stripped from the VIRTUAL_ENV value (printf | tr -d '\n\r') before it is written to "$GITHUB_ENV", which is now quoted.

