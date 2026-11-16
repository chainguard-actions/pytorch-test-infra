<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose uses: refs point at a mutable branch instead of a 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes a value built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV without first sanitising it: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. The script reads RUNNER_TEMP but never sets it, and there is no printf '%s' ... | tr -d '\n\r' step before the write.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml.

1. Pinned actions: the setup-uv and get-workflow-job-id steps referenced the moving `main` branch. Both now point at pytorch/test-infra commit 6f7274a0eff04dd4f8ada574e4e144610cece2c8, which is the upstream commit this mirror was built from. I confirmed the SHA with lookup_action_sha and kept a `# main` comment so the original ref is still visible.

2. Writes to $GITHUB_ENV: the VIRTUAL_ENV value built from RUNNER_TEMP now has newlines and carriage returns stripped (`printf '%s' ... | tr -d '\n\r'`) before it is written, and `$GITHUB_ENV` is now quoted. I made the same change to the DEVICE_TYPE write in the 'Get device type' step, which wasn't in the findings. That value comes from command output, so it seemed worth covering too.

Nothing was run or tested after the edits.

