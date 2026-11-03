<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--trigger-nightly/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--trigger-nightly/v20261027-001733** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step uses a version tag instead of a full 40-character commit SHA: `uses: actions/checkout@v4`.

Locations:

- `action.yml:22`

### script-injection (severity: high)

Sub-rule (a): an expression is placed directly in the run script: `pushd ${{ inputs.path }}`. A malicious `path` input becomes shell code. Fix: set PATH_INPUT: ${{ inputs.path }} in the step's env: block and use `pushd "$PATH_INPUT"`.

Locations:

- `action.yml:31`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.path }}" appears directly in run: block of step "Create nightly commit"; move to env: map

Locations:

- `action.yml:31`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection

**Notes:**

Pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). Moved inputs.path into the env var PATH_INPUT in the 'Create nightly commit' step and quoted it as pushd "$PATH_INPUT".

### Iteration 2

**Fixes applied:** unpinned-uses

**Notes:**

Pinned actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262 # v4 in action.yml.

