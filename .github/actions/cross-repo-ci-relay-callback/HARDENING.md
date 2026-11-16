<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261109-192709** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

In action.yml, the composite step pins actions/github-script to a mutable tag instead of a full 40-character commit SHA: `uses: actions/github-script@v9`. Pin it to a commit SHA, e.g. `actions/github-script@<sha> # v9`.

Locations:

- `action.yml:164`

### script-injection (severity: high)

Sub-rule (a): a GitHub Actions expression is placed directly inside a run: script in the 'Send callback to relay server' step: `run: python3 "${{ github.action_path }}/report_callback.py"`. Pass it in through env instead (e.g. `ACTION_PATH: ${{ github.action_path }}`) and reference it as "$ACTION_PATH", or use the runner-provided "$GITHUB_ACTION_PATH".

Locations:

- `action.yml:224`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection

**Notes:**

Pinned actions/github-script@v9 to 3a2844b7e9c422d3c10d287c895573f7108da1b3 (# v9). Replaced inline ${{ github.action_path }} in bash run with runner-provided "$GITHUB_ACTION_PATH".

