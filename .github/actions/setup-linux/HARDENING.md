<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261109-232755** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step pins to a branch instead of a 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited env var RUNNER_TEMP. It then writes them to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`) without first running `printf '%s' ... | tr -d '\n\r'`. RUNNER_TEMP is normally set by the runner itself, but this check treats any inherited env var in a composite action as untrusted, so a newline in it could inject extra env entries.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Fixed both findings in action.yml.

1. unpinned-uses: `pytorch/test-infra/.github/actions/setup-nvidia@main` now points to a full commit SHA, `2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f # main`. That is the upstream commit this mirror was built from, so the nvidia setup step runs the same code as the rest of the action. Today's tip of main (31bc75abe7…) has moved past it, and I chose not to use that.

2. github-env-injection: before writing RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR to $GITHUB_ENV, the step now strips newline and carriage-return characters with `printf '%s' ... | tr -d '\n\r'`. The directory create and delete commands, and the values written in the normal case, are unchanged.

I haven't run the action after these edits.

