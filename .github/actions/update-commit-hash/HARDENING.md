<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-commit-hash/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-commit-hash/v20261125-022556** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Checkout the target repo' step puts GitHub expressions straight into the run: script: `git clone https://github.com/${{ inputs.repo-owner }}/${{ inputs.repo-name }}.git --quiet`. A caller who controls these inputs can add shell metacharacters and run their own commands. Fix: pass the values in through env: variables and use them double-quoted.

Locations:

- `action.yml:60`

### unpinned-uses (severity: high)

action.yml references actions by version tag instead of a full 40-character commit SHA: `uses: actions/checkout@v4` (twice) and `uses: actions/setup-python@v5`.

Locations:

- `action.yml:45`
- `action.yml:52`
- `action.yml:62`

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

**Fixes applied:** script-injection, unpinned-uses, static-inline-injection

**Notes:**

Pinned actions/checkout (used twice) to 11d5960a326750d5838078e36cf38b85af677262 # v4 and actions/setup-python to a26af69be951a213d495a4c3e4e4022e16d87065 # v5. In the 'Checkout the target repo' step, moved inputs.repo-owner and inputs.repo-name into env (REPO_OWNER, REPO_NAME) and put the clone URL in double quotes.

