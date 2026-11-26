<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references composite steps by a mutable branch instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:119`

### github-env-injection (severity: high)

The 'Install dependencies' step writes a value built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV with no sanitization: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is read from the environment, not set by this script. This check requires running printf '%s' ... | tr -d '\n\r' on the value just before the write, and quoting "$GITHUB_ENV".

Locations:

- `action.yml:42`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I pinned both pytorch/test-infra sub-action references (setup-uv and get-workflow-job-id) to full commit SHA f2f972bd8f3eab11aa0094897a81879653c6f141, which I confirmed with lookup_action_sha. This is the request's upstream_commit, the commit this mirror was built from, so the sub-actions now run at the same commit as the action itself. Before, they followed whatever upstream's main branch held at run time. Each line keeps a '# main' comment showing the branch it used to follow. In 'Install dependencies', VIRTUAL_ENV now has newlines stripped with printf '%s' | tr -d '\n\r' before it is written, and $GITHUB_ENV is quoted. Two extras beyond the findings: I quoted $GITHUB_ENV where DEVICE_NAME is written, and I applied the same newline strip to DEVICE_TYPE, since that value comes from command output. Nothing was run to test these edits.

