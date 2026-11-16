<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-commit-hash/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-commit-hash/v20261112-155209** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose uses: refs are version tags, not full 40-character commit SHAs: 'uses: actions/checkout@v4' (line 45), 'uses: actions/checkout@v4' (line 52), 'uses: actions/setup-python@v5' (line 63).

Locations:

- `action.yml:45`
- `action.yml:52`
- `action.yml:63`

### script-injection (severity: high)

Rule (a), direct expression interpolation: the 'Checkout the target repo' step puts inputs straight into the run: script: 'git clone https://github.com/${{ inputs.repo-owner }}/${{ inputs.repo-name }}.git --quiet'. A caller can pass shell metacharacters in repo-owner or repo-name and run any command. Fix: move them into env: (e.g. REPO_OWNER, REPO_NAME) and use "https://github.com/${REPO_OWNER}/${REPO_NAME}.git" in double quotes.

Locations:

- `action.yml:61`

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

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection

**Notes:**

Pinned both actions/checkout@v4 uses to 11d5960a326750d5838078e36cf38b85af677262 and actions/setup-python@v5 to a26af69be951a213d495a4c3e4e4022e16d87065, with the tag kept in a trailing comment. The 'Checkout the target repo' step no longer puts inputs.repo-owner and inputs.repo-name straight into its run: script. They now go in through env: as REPO_OWNER and REPO_NAME, and the git clone uses the double-quoted URL "https://github.com/${REPO_OWNER}/${REPO_NAME}.git". Nothing was run to test these changes.

