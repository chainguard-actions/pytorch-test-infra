<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261119-192116** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step in action.yml points `uses:` at a branch, not a commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs. Pin it to the full 40-character commit SHA.

Locations:

- `action.yml:89`

### github-env-injection (severity: high)

The step 'Setup useful environment variables' builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var ${RUNNER_TEMP}. This script does not set RUNNER_TEMP; it comes from outside, so in a composite action it counts as workflow-controlled. The values are written straight to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`) without first stripping newlines with `printf '%s' ... | tr -d '\n\r'`.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml.

- **unpinned-uses:** the setup-nvidia step pointed at the `main` branch. It is now pinned to `pytorch/test-infra/.github/actions/setup-nvidia@7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4 # main`. That SHA is upstream_commit from the request, the test-infra commit this version was built from. I did not resolve the current tip of `main` with lookup_action_sha, so the sub-action runs as it was at that commit, not as it is on `main` today.
- **github-env-injection:** the 'Setup useful environment variables' step now strips newlines from `RUNNER_TEMP` (using `printf '%s' | tr -d '\n\r'`) and builds the three directory paths from the cleaned value. Each value is cleaned again right before it is written to `$GITHUB_ENV`. Each value is captured on its own line, so no command's exit status is hidden. The `rm` and `mkdir` steps work as before.

I haven't run the edited action or re-run the analysis.

