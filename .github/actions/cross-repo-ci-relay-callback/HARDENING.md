<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20260922-155642** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action step pulls in an action by a mutable tag instead of a full 40-character commit SHA: `uses: actions/github-script@v9`. Whoever controls that tag can change the code this step runs. Pin it to a commit SHA, e.g. `actions/github-script@<40-hex-sha> # v9`.

Locations:

- `action.yml:134`

### script-injection (severity: high)

Sub-rule (a): a GitHub Actions expression is inserted directly into a run: script in the 'Send callback to relay server' step. Offending line: `run: python3 "${{ github.action_path }}/report_callback.py"`. Any `${{ ... }}` inside a run: block is substituted into the script text before the shell parses it. Use the runner-provided `$GITHUB_ACTION_PATH` env var instead, double-quoted: `python3 "$GITHUB_ACTION_PATH/report_callback.py"`.

Locations:

- `action.yml:187`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection

**Notes:**

Pinned actions/github-script@v9 to 3a2844b7e9c422d3c10d287c895573f7108da1b3 (# v9). Replaced inline ${{ github.action_path }} in run: with the runner-provided "$GITHUB_ACTION_PATH" (shell: bash).

