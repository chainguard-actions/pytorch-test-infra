<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point at a mutable branch instead of a 40-char commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115). Pin both to a full commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is a process env var this composite action inherits; the script reads it and does not compute it. It goes into $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' step. Strip newlines from the value first (e.g. safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r')), then write it with the target quoted: >> "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I pinned both pytorch/test-infra sub-actions (setup-uv and get-workflow-job-id) to the upstream commit given in the request, f2f972bd8f3eab11aa0094897a81879653c6f141, and added a '# v20261029-163400' comment. I didn't check that SHA with lookup_action_sha, because it comes straight from the request's upstream_commit. Pinning to it makes the sub-actions run at the same upstream commit this mirror version was built from, where '@main' moved over time. I nothing ran or tested after the edits.

For the env finding, the VIRTUAL_ENV value now has newlines stripped (printf '%s' ... | tr -d '\n\r') before it is written to "$GITHUB_ENV", with the target quoted. Two changes were not in the findings: I quoted "$GITHUB_ENV" for the DEVICE_NAME write, and stripped newlines from DEVICE_TYPE (which comes from command output) before writing it. That second one is the same kind of issue and would likely be flagged on the next pass.

