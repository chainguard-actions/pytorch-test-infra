<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Two composite steps in action.yml reference actions by the mutable branch ref @main instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 114). Anyone who can push to that branch can change what code runs.

Locations:

- `action.yml:31`
- `action.yml:114`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is an inherited process env var, not a value computed in this run: script, and it is not passed through printf '%s' ... | tr -d '\n\r' first. Under rule (e), a calling workflow could set this value to include newlines and inject extra variables into GITHUB_ENV. $GITHUB_ENV is also left unquoted.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml.

- **unpinned-uses:** The `setup-uv` and `get-workflow-job-id` steps used `@main`. Both now point to 9206d491d3a5507163cb9d5b77040d4c3ef5e038 with a `# main` comment. That is the upstream commit this version was built from, and I confirmed it with lookup_action_sha.
- **github-env-injection:** The `VIRTUAL_ENV` value written to `$GITHUB_ENV` now goes through `printf '%s' ... | tr -d '\n\r'` first, and `$GITHUB_ENV` is quoted.

I made two extra changes that weren't in the findings. The `DEVICE_TYPE` value, which comes from command output, now has newlines stripped before it is written. The `DEVICE_NAME` and `DEVICE_TYPE` writes now quote `"$GITHUB_ENV"`. The assignments are left as their own statements, so a failing command still stops the step under `set -e`. Nothing was run to test these changes.

