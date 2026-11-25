<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Two composite steps in action.yml point at a mutable branch (@main) instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115). Whoever controls that branch can change the code these steps run, which makes this a supply-chain risk. The second step also receives inputs.github-token.

Locations:

- `action.yml:31`
- `action.yml:115`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id from @main to 13fc79c71b9a7c86a46d898782991a6418778f0b, the upstream commit this version was built from. I checked the SHA with lookup_action_sha, and each line keeps a trailing comment naming the ref. Nothing else in the file was changed.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In action.yml, the 'Install dependencies' step no longer writes VIRTUAL_ENV straight to $GITHUB_ENV. It now runs the value through printf '%s' ... | tr -d '\n\r', saves it as safe_venv, and writes that to the quoted "$GITHUB_ENV". I also changed one write the finding didn't list: 'Get device type' puts command output into DEVICE_TYPE before writing it to $GITHUB_ENV, so it now strips newlines in the same way. I quoted $GITHUB_ENV in the DEVICE_NAME write too; that value is always one of a few fixed words. Each command still runs in its own assignment, so a failing command still stops the step. I didn't test any of these changes.

