<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references composite steps by a mutable branch ref instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:114`

### github-env-injection (severity: high)

The 'Install dependencies' step writes a value built from the inherited env var RUNNER_TEMP to $GITHUB_ENV with no sanitization: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. The script reads RUNNER_TEMP rather than setting it, so under this check it counts as an untrusted source. The value needs the printf '%s' ... | tr -d '\n\r' step right before the write, and $GITHUB_ENV should be quoted.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I pinned both `uses:` lines in action.yml (pytorch/test-infra setup-uv and get-workflow-job-id) to bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c, with a `# main` comment. That SHA is the upstream commit this mirror version was built from, taken from the request. I did not look it up with lookup_action_sha, and pinning to current `main` would have given a different commit. In the 'Install dependencies' step, the VIRTUAL_ENV value built from RUNNER_TEMP now goes through `printf '%s' ... | tr -d '\n\r'` before it is written, and $GITHUB_ENV is quoted. Two changes go beyond the findings: I quoted $GITHUB_ENV in the DEVICE_NAME write, and I added the same newline stripping to the DEVICE_TYPE write. Nothing was run to test these changes.

