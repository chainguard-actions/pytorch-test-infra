<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261109-232755** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step points to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs. Pin it to a commit SHA.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var RUNNER_TEMP. It then writes each one to $GITHUB_ENV without sanitizing it first, e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. RUNNER_TEMP is not set inside this run: script, so the check counts it as workflow-controlled. Run each value through `printf '%s' ... | tr -d '\n\r'` before writing it.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned the setup-nvidia step (pytorch/test-infra/.github/actions/setup-nvidia@main) to 2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f, with a '# main' comment. That is the request's upstream_commit, the test-infra commit this mirror was built from. I took it from the request instead of calling lookup_action_sha. The step now runs setup-nvidia from that same commit instead of whatever main points to today. The 'Setup useful environment variables' step now passes RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR through printf '%s' ... | tr -d '\n\r' before writing each one to $GITHUB_ENV. Nothing else changed, and I didn't run the action to test the edits.

