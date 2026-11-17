<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261112-155209** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite step points to a mutable tag instead of a full 40-character commit SHA: `uses: actions/github-script@v9`. Pin it to a commit SHA, for example `actions/github-script@<sha> # v9`.

Locations:

- `action.yml:183`

### script-injection (severity: high)

Rule (a) violation: a GitHub Actions expression is placed straight into a run: shell command in the 'Send callback to relay server' step: `run: python3 "${{ github.action_path }}/report_callback.py"`. Use the shell variable instead: `python3 "$GITHUB_ACTION_PATH/report_callback.py"`.

Locations:

- `action.yml:236`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection

**Notes:**

Pinned actions/github-script to the commit SHA 3a2844b7e9c422d3c10d287c895573f7108da1b3 (# v9). In the bash run step, replaced ${{ github.action_path }} with $GITHUB_ACTION_PATH. Nothing was run to test these changes.

