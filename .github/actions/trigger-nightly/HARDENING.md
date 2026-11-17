<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--trigger-nightly/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--trigger-nightly/v20261109-192709** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the expression is placed straight into the run script: `pushd ${{ inputs.path }}`. A caller-supplied path containing shell metacharacters would run as commands. Fix: set PATH_INPUT: ${{ inputs.path }} in the step's env: block and use `pushd "$PATH_INPUT"`.

Locations:

- `action.yml:31`

### unpinned-uses (severity: high)

This composite step uses a version tag instead of a full commit SHA: `uses: actions/checkout@v4`. Pin it to a 40-character commit SHA.

Locations:

- `action.yml:22`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.path }}" appears directly in run: block of step "Create nightly commit"; move to env: map

Locations:

- `action.yml:31`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, static-inline-injection, unpinned-uses

**Notes:**

Pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). Moved inputs.path into env PATH_INPUT and used pushd "$PATH_INPUT" in the run script.

