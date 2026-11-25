<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite step references an action by a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

Step 'Setup useful environment variables' writes values built from the inherited process env var RUNNER_TEMP (RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR, RUNNER_DOCS_DIR) to $GITHUB_ENV, e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. RUNNER_TEMP is not set by this script, and the values are not run through `printf '%s' ... | tr -d '\n\r'` before the write.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in action.yml. I haven't run the action or any tests on these changes.

1. Unpinned action: the step `pytorch/test-infra/.github/actions/setup-nvidia@main` now points at the full commit SHA 9206d491d3a5507163cb9d5b77040d4c3ef5e038, with a comment saying it was upstream main at build time. I took that SHA from the request's upstream_commit, which is the commit this setup-linux action was built from. I didn't use lookup_action_sha, because today's main may no longer match that build. The NVIDIA setup no longer follows upstream main and stays fixed at that commit.

2. Unsafe writes to GITHUB_ENV: in the 'Setup useful environment variables' step, RUNNER_TEMP now has newlines and carriage returns removed before it is used. RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR are each cleaned the same way just before they are written to $GITHUB_ENV. Each value is captured in a plain assignment, so if a command fails the step still stops as before. On a normal runner the paths and directories created are the same as before.

