<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-commit-hash/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-commit-hash/v20261027-001733** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a), direct expression interpolation, in step 'Checkout the target repo'. The offending line is `git clone https://github.com/${{ inputs.repo-owner }}/${{ inputs.repo-name }}.git --quiet`. The caller supplies these inputs, and their values are pasted into the shell script before bash runs it. Fix: move them into env: variables (e.g. REPO_OWNER and REPO_NAME) and reference them double-quoted: `git clone "https://github.com/${REPO_OWNER}/${REPO_NAME}.git" --quiet`.

Locations:

- `action.yml:61`

### unpinned-uses (severity: high)

Three composite steps reference actions by a mutable tag instead of a full 40-character commit SHA: `uses: actions/checkout@v4` (line 45), `uses: actions/checkout@v4` (line 52) and `uses: actions/setup-python@v5` (line 63). Pin each one to a full commit SHA, with the version as a trailing comment.

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

I made two changes to action.yml and haven't run the action since.

1. Script injection: the 'Checkout the target repo' step no longer pastes inputs.repo-owner and inputs.repo-name into the shell script. They now go into the step's env: block as REPO_OWNER and REPO_NAME, and the clone command uses them double-quoted: git clone "https://github.com/${REPO_OWNER}/${REPO_NAME}.git" --quiet.

2. Pinned actions: I looked up the commit for each tag and pinned both actions/checkout steps to 11d5960a326750d5838078e36cf38b85af677262 (v4) and actions/setup-python to a26af69be951a213d495a4c3e4e4022e16d87065 (v5). The version is kept as a trailing comment on each line.

