<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-commit-hash/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-commit-hash/v20261029-163400** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Checkout the target repo' step puts inputs.repo-owner and inputs.repo-name directly into a run: script: `git clone https://github.com/${{ inputs.repo-owner }}/${{ inputs.repo-name }}.git --quiet`. Whoever sets these inputs can run their own shell commands. Fix: pass the values in through env: variables and use them double-quoted, e.g. "https://github.com/${REPO_OWNER}/${REPO_NAME}.git".

Locations:

- `action.yml:62`

### unpinned-uses (severity: high)

These composite steps use tags instead of 40-character commit SHAs: `uses: actions/checkout@v4` (twice) and `uses: actions/setup-python@v5`.

Locations:

- `action.yml:46`
- `action.yml:53`
- `action.yml:64`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.repo-owner }}" appears directly in run: block of step "Checkout the target repo"; move to env: map

Locations:

- `action.yml:61`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.repo-name }}" appears directly in run: block of step "Checkout the target repo"; move to env: map

Locations:

- `action.yml:61`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, static-inline-injection, unpinned-uses

**Notes:**

In action.yml, the 'Checkout the target repo' step no longer puts inputs.repo-owner and inputs.repo-name straight into the run: script. They now come in through env: as REPO_OWNER and REPO_NAME, and the clone URL uses them double-quoted. The two actions/checkout steps are pinned to 11d5960a326750d5838078e36cf38b85af677262 (# v4) and setup-python to a26af69be951a213d495a4c3e4e4022e16d87065 (# v5); both SHAs came from lookup_action_sha. No other lines were changed, and nothing was run or tested.

