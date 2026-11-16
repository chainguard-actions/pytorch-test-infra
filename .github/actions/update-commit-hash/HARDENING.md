<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-commit-hash/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-commit-hash/v20261021-234439** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Checkout the target repo' step puts input expressions straight into the run: script: `git clone https://github.com/${{ inputs.repo-owner }}/${{ inputs.repo-name }}.git --quiet`. Whoever calls the action controls these inputs, so shell metacharacters in them run as commands. Fix: pass the inputs through env: variables (e.g. REPO_OWNER, REPO_NAME) and reference them double-quoted, e.g. "https://github.com/${REPO_OWNER}/${REPO_NAME}.git".

Locations:

- `action.yml:61`

### unpinned-uses (severity: high)

The composite steps reference actions by mutable tags instead of 40-character commit SHAs: `uses: actions/checkout@v4` (line 45), `uses: actions/checkout@v4` (line 52), `uses: actions/setup-python@v5` (line 63).

Locations:

- `action.yml:45`
- `action.yml:52`
- `action.yml:63`

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

In action.yml, the 'Checkout the target repo' step no longer puts inputs.repo-owner and inputs.repo-name straight into the script. They now go through env: (REPO_OWNER, REPO_NAME), and the clone URL uses them inside double quotes. I pinned both actions/checkout@v4 references to 11d5960a326750d5838078e36cf38b85af677262 and actions/setup-python@v5 to a26af69be951a213d495a4c3e4e4022e16d87065, each with a trailing # tag comment. I got the SHAs from lookup_action_sha. I didn't run the action or a fresh analysis pass after the edits.

