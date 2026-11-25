<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261125-022556** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that points to a branch, not a full commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch changes the code this action runs. Pin it to a 40-character commit SHA.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from ${RUNNER_TEMP}. This step never sets RUNNER_TEMP; the composite action inherits it from the calling environment. The values are then written to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`) without first running `printf '%s' ... | tr -d '\n\r'`. A newline in the inherited value could inject extra environment variables.

Locations:

- `action.yml:67`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in action.yml.

1. unpinned-uses: the setup-nvidia step pointed at the `main` branch. It now points at commit 13fc79c71b9a7c86a46d898782991a6418778f0b, with `# main` kept as a comment. I looked up the SHA for `main` and it is the same commit as this release's upstream_commit, so the step still runs the same code it did when this version was built.

2. github-env-injection: the 'Setup useful environment variables' step now strips newlines and carriage returns before writing to $GITHUB_ENV. RUNNER_TEMP is cleaned with `printf '%s' ... | tr -d '\n\r'` before the three directories are built from it, and each value is cleaned again just before its `echo` into $GITHUB_ENV. The directory names and the `sudo rm -rf` / `mkdir -p` commands are unchanged. On a normal runner, RUNNER_TEMP has no newlines, so the paths come out exactly as before.

I haven't run the action or the analysis again after these edits.

