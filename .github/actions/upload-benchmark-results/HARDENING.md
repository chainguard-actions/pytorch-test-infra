<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that use branch refs instead of full 40-character commit SHAs: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 126). Whoever controls the main branch decides what code runs in this action.

Locations:

- `action.yml:31`
- `action.yml:126`

### github-env-injection (severity: high)

The 'Install dependencies' step runs 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is a process env var the composite action inherits; this script reads it and does not compute it. It goes into $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' sanitization the check requires right before the write. The runner normally sets RUNNER_TEMP itself, so the real-world risk is low, but this still fails the check as written. Fix: safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'); echo "VIRTUAL_ENV=$safe" >> "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I pinned both sub-actions in action.yml, setup-uv and get-workflow-job-id. They now point to pytorch/test-infra@6f7274a0eff04dd4f8ada574e4e144610cece2c8 # main instead of the main branch. That is the upstream commit this mirror was built from, so the sub-actions match the rest of the action. lookup_action_sha confirmed the SHA exists in pytorch/test-infra; I didn't look up where main points now, and I didn't run the action. In the 'Install dependencies' step, the VIRTUAL_ENV value now has newlines stripped with printf '%s' | tr -d '\n\r' before it is written to $GITHUB_ENV, and $GITHUB_ENV is now quoted. The findings didn't ask for this, but I did the same to the DEVICE_TYPE write, since that value comes from command output. DEVICE_NAME is still written as before; it is always a fixed word the script sets itself.

