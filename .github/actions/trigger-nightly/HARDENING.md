<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--trigger-nightly/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--trigger-nightly/v20261109-232755** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite step uses a mutable tag ref: 'uses: actions/checkout@v4'. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:22`

### script-injection (severity: high)

Rule (a): the 'Create nightly commit' step puts an expression straight into the run: script: 'pushd ${{ inputs.path }}'. Move inputs.path into an env: variable and use it quoted, e.g. pushd "$INPUT_PATH".

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

Pinned actions/checkout to commit 11d5960a326750d5838078e36cf38b85af677262, the commit the v4 tag points to; the '# v4' comment stays so the version is still readable. In the 'Create nightly commit' step, inputs.path now comes in through the step's env: as INPUT_PATH, and the script runs pushd "$INPUT_PATH" (quoted) instead of putting the expression straight into the script. Nothing was run to test these edits.

