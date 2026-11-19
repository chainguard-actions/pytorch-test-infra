<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a `uses:` reference pinned to a branch rather than a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Pin it to a specific commit SHA.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The step 'Setup useful environment variables' builds values from the inherited process env var RUNNER_TEMP, which the composite action reads but does not set itself, and writes them to $GITHUB_ENV without the `printf '%s' ... | tr -d '\n\r'` sanitization step. The lines are `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`, and the same pattern for RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR. Strip newlines from the value before each write.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in hardened/action/action.yml.

1. unpinned-uses: `pytorch/test-infra/.github/actions/setup-nvidia@main` now points to bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c, with a comment saying it was `main`. That SHA is the request's upstream_commit, the test-infra commit this action version was built from, so the nested action matches the code it shipped with. I took it from the request instead of looking it up, because looking up `main` would return today's head, not that commit.

2. github-env-injection: in 'Setup useful environment variables', the step now strips newlines from RUNNER_TEMP once at the start (SAFE_RUNNER_TEMP) and builds the three directory paths from that. Each write to $GITHUB_ENV also strips newlines again with `printf '%s' ... | tr -d '\n\r'`. The mkdir, rm and env values all use the same cleaned path, so they still agree. Nothing else in the step changed.

