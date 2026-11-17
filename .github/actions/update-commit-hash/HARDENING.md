<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-commit-hash/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-commit-hash/v20261021-234439** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose uses: references point to mutable tags, not 40-character commit SHAs: 'uses: actions/checkout@v4' (line 45), 'uses: actions/checkout@v4' (line 52), 'uses: actions/setup-python@v5' (line 63).

Locations:

- `action.yml:45`
- `action.yml:52`
- `action.yml:63`

### script-injection (severity: high)

Rule (a), direct expression interpolation: the 'Checkout the target repo' step puts input expressions straight into the run: script: 'git clone https://github.com/${{ inputs.repo-owner }}/${{ inputs.repo-name }}.git --quiet'. Move these inputs into env: variables (e.g. REPO_OWNER, REPO_NAME) and use them double-quoted: git clone "https://github.com/${REPO_OWNER}/${REPO_NAME}.git" --quiet.

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

Pinned actions/checkout@v4 (both uses) to 11d5960a326750d5838078e36cf38b85af677262 and actions/setup-python@v5 to a26af69be951a213d495a4c3e4e4022e16d87065, keeping the tag as a trailing comment. In the 'Checkout the target repo' step, moved inputs.repo-owner and inputs.repo-name into env (REPO_OWNER, REPO_NAME). The git clone URL now uses them inside double quotes.

