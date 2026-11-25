<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261112-155209** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step points to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs. Pin it to a commit SHA.

Locations:

- `action.yml:88`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds three values from the inherited process env var RUNNER_TEMP, which this script reads but does not set. It writes them to $GITHUB_ENV without cleaning them first: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`, and the same for RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR. The check requires `printf '%s' ... | tr -d '\n\r'` before each write. Without it, a value containing a newline could add extra variables to the environment.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in action.yml.

1. **unpinned-uses:** The step that installs the NVIDIA driver now pins pytorch/test-infra/.github/actions/setup-nvidia to 6f7274a0eff04dd4f8ada574e4e144610cece2c8, with a '# main' comment for readability. That SHA is the upstream_commit given in the request, so the sub-action comes from the same pytorch/test-infra commit this release was built from. I did not run lookup_action_sha on main. Today's main may point to a newer commit, and choosing this one was deliberate.

2. **github-env-injection:** In the 'Setup useful environment variables' step, RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now each go through `printf '%s' ... | tr -d '\n\r'` before being written to $GITHUB_ENV. The directory setup (rm -rf / mkdir -p) still uses the original values, as upstream did.

I did not run or test the action after these edits.

