<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--trigger-nightly/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--trigger-nightly/v20261112-155209** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite step uses a mutable tag instead of a full commit SHA: 'uses: actions/checkout@v4'.

Locations:

- `action.yml:22`

### script-injection (severity: high)

Rule (a): a GitHub expression is interpolated straight into the run: script of the 'Create nightly commit' step: 'pushd ${{ inputs.path }}'. The input value is inserted into the script text before bash runs, so shell metacharacters in it can execute commands. Fix: pass it through env (e.g. INPUT_PATH: ${{ inputs.path }}) and use pushd "$INPUT_PATH".

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

Pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). Moved inputs.path to env INPUT_PATH and used pushd "$INPUT_PATH".

