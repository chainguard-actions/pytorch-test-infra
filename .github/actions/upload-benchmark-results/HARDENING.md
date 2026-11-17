<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose uses: refs point to a mutable branch, not a 40-char commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is a process env var the composite action inherits and does not set itself, so under this check it counts as workflow-controlled. It goes into $GITHUB_ENV without first being cleaned with printf '%s' ... | tr -d '\n\r'. The $GITHUB_ENV path is also left unquoted.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned both same-repo sub-actions (setup-uv, get-workflow-job-id) to e9b5b0a4c36ebfde49dec880ae77705038009471, the upstream commit this mirror version was built from, and kept '# main' as a comment. The VIRTUAL_ENV value now has newlines and carriage returns stripped (printf | tr -d '\n\r') before it is written to the env file, and $GITHUB_ENV is quoted. I also made two changes that weren't in the findings: quoted $GITHUB_ENV in the DEVICE_NAME write, and stripped newlines from DEVICE_TYPE before writing it.

