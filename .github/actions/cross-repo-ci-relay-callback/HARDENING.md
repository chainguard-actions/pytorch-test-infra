<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step uses an action by a mutable tag instead of a full 40-character commit SHA: `uses: actions/github-script@v9`.

Locations:

- `action.yml:130`

### script-injection (severity: high)

Sub-rule (a): an expression is placed directly inside the run: command of the 'Send callback to relay server' step: `run: python3 "${{ github.action_path }}/report_callback.py"`. Use the $GITHUB_ACTION_PATH env var instead (e.g. `python3 "$GITHUB_ACTION_PATH/report_callback.py"`).

Locations:

- `action.yml:184`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection

**Notes:**

Pinned actions/github-script@v9 to 3a2844b7e9c422d3c10d287c895573f7108da1b3 (# v9). Replaced the ${{ github.action_path }} expression in the bash run step with "$GITHUB_ACTION_PATH".

