<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261109-232755** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step points to a version tag, not a full 40-character commit SHA: `uses: actions/github-script@v9`. A tag can be moved to different code later. Pin it to a commit SHA.

Locations:

- `action.yml:225`

### script-injection (severity: high)

Rule (a): an expression is put straight into a run: block in the 'Send callback to relay server' step: `run: python3 "${{ github.action_path }}/report_callback.py"`. Use the GITHUB_ACTION_PATH env var instead, double-quoted: "$GITHUB_ACTION_PATH/report_callback.py".

Locations:

- `action.yml:285`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection

**Notes:**

Pinned actions/github-script@v9 to commit 3a2844b7e9c422d3c10d287c895573f7108da1b3, keeping '# v9' as a comment. In the bash step 'Send callback to relay server', replaced ${{ github.action_path }} with "$GITHUB_ACTION_PATH" (double-quoted), which the runner sets for that step. These were the only two places in action.yml that matched. No tests were run.

