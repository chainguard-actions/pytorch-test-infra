<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-commit-hash/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-commit-hash/v20261109-192709** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose `uses:` references point to mutable tags instead of 40-character commit SHAs: `uses: actions/checkout@v4` (line 45), `uses: actions/checkout@v4` (line 52), `uses: actions/setup-python@v5` (line 63).

Locations:

- `action.yml:45`
- `action.yml:52`
- `action.yml:63`

### script-injection (severity: high)

Rule (a) is violated: expressions are placed directly into a run: script in the 'Checkout the target repo' step: `git clone https://github.com/${{ inputs.repo-owner }}/${{ inputs.repo-name }}.git --quiet`. Whoever sets inputs.repo-owner or inputs.repo-name can inject shell commands. Fix: pass these values in through env: variables and expand them double-quoted, e.g. `git clone "https://github.com/${REPO_OWNER}/${REPO_NAME}.git" --quiet`.

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

Pinned both actions/checkout@v4 uses and actions/setup-python@v5 to full commit SHAs, with the tag kept as a comment. In the 'Checkout the target repo' step, inputs.repo-owner and inputs.repo-name now come in through the step's env: block as REPO_OWNER and REPO_NAME. The git clone URL now uses those variables inside double quotes. Not tested.

