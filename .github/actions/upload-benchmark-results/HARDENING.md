<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261021-234439** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by a branch name instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step runs 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is a process env var that this script reads but does not set, and a composite action inherits it from the calling workflow. The value goes into $GITHUB_ENV without first passing through printf '%s' ... | tr -d '\n\r', and $GITHUB_ENV is unquoted.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in action.yml.

- unpinned-uses: The setup-uv and get-workflow-job-id steps referenced @main. Both are now pinned to pytorch/test-infra@4bb924e6cddf98370d0c754d6769b492fe457233 # main. That is the upstream commit this mirror version was built from, and I confirmed with lookup_action_sha that it resolves.
- github-env-injection: The VIRTUAL_ENV value is now passed through printf '%s' | tr -d '\n\r' before it is written, and $GITHUB_ENV is quoted.

I also made two changes the findings didn't ask for. The DEVICE_TYPE value, which comes from command output, now has newlines stripped the same way before it goes into $GITHUB_ENV. The DEVICE_NAME and DEVICE_TYPE writes also quote $GITHUB_ENV now.

Nothing else changed, and I haven't run the action to test these edits.

