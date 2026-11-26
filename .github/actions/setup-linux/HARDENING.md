<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that points `uses:` at a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this step runs.

Locations:

- `action.yml:91`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds three values from the inherited process env var RUNNER_TEMP and writes them to $GITHUB_ENV with no `printf '%s' ... | tr -d '\n\r'` step first. RUNNER_TEMP is not set in this script, so under this check it counts as workflow-controlled. The writes are `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`, and the same pattern for RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in action.yml. I haven't run the action to test the changes.

1. **unpinned-uses:** The nested `pytorch/test-infra/.github/actions/setup-nvidia@main` step now points at commit e9b5b0a4c36ebfde49dec880ae77705038009471. That's the upstream commit this version is built from, and I confirmed it with lookup_action_sha. A `# main` comment is kept for readability. This doesn't match upstream exactly: upstream follows whatever `main` is at run time, and this always runs the setup-nvidia code from that one commit.

2. **github-env-injection:** In the 'Setup useful environment variables' step, `RUNNER_TEMP` now has newlines and carriage returns stripped once, up front. Each of `RUNNER_ARTIFACT_DIR`, `RUNNER_TEST_RESULTS_DIR` and `RUNNER_DOCS_DIR` is also passed through `printf '%s' | tr -d '\n\r'` before it's written to `$GITHUB_ENV`. The directories created and the values written are the same as before unless `RUNNER_TEMP` actually contains a newline.

