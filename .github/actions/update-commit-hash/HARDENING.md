<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-commit-hash/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-commit-hash/v20261027-001733** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses actions by mutable tag instead of a full 40-character commit SHA: 'uses: actions/checkout@v4' (line 45), 'uses: actions/checkout@v4' (line 52), 'uses: actions/setup-python@v5' (line 63).

Locations:

- `action.yml:45`
- `action.yml:52`
- `action.yml:63`

### script-injection (severity: high)

Rule (a) is violated: GitHub expressions are placed directly inside a run: script in the 'Checkout the target repo' step: 'git clone https://github.com/${{ inputs.repo-owner }}/${{ inputs.repo-name }}.git --quiet'. The values of inputs.repo-owner and inputs.repo-name are pasted into the script before the shell runs it, so shell metacharacters in them would run as commands. Fix: pass them in through env: (e.g. REPO_OWNER, REPO_NAME) and quote them: git clone "https://github.com/${REPO_OWNER}/${REPO_NAME}.git" --quiet.

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

I pinned both actions/checkout@v4 references to 11d5960a326750d5838078e36cf38b85af677262 and actions/setup-python@v5 to a26af69be951a213d495a4c3e4e4022e16d87065. Each pin keeps a comment naming its tag. In the 'Checkout the target repo' step, inputs.repo-owner and inputs.repo-name now come in through the step's env: as REPO_OWNER and REPO_NAME, and the clone URL that uses them is double-quoted. I didn't run anything to test these changes.

