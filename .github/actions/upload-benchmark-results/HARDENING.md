<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point at a mutable branch instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is inherited from the process environment, not set by this script. In a composite action, the calling workflow controls inherited env vars. The value is written to $GITHUB_ENV without first running printf '%s' ... | tr -d '\n\r', and $GITHUB_ENV is not quoted.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml. Nothing was run to test the changes.

- **Unpinned uses:** the setup-uv and get-workflow-job-id steps used to point at the `main` branch. They now point at commit e9b5b0a4c36ebfde49dec880ae77705038009471, with a `# main` comment kept for readability. I took that commit from the request's upstream_commit (the commit this mirror version was built from), not from `lookup_action_sha`, so the sub-actions run at the same code as the parent action. They will not follow later changes to `main`.
- **GITHUB_ENV injection:** the value written as `VIRTUAL_ENV` now has newlines and carriage returns stripped (`printf '%s' | tr -d '\n\r'`) before it goes into `"$GITHUB_ENV"`, which is now quoted.
- **Extra changes beyond the two findings:** in the "Get device name" and "Get device type" steps I also quoted `"$GITHUB_ENV"`. In the "Get device type" step I strip newlines from `DEVICE_TYPE` the same way, since it comes from command output.

