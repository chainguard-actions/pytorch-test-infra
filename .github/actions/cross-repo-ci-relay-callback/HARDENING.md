<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action step uses a version tag instead of a full 40-character commit SHA: `uses: actions/github-script@v9`. Whoever controls that tag can move it to different code, so pin it to a commit SHA.

Locations:

- `action.yml:169`

### script-injection (severity: high)

Rule (a): an expression is placed directly into a run: script. The offending line is `run: python3 "${{ github.action_path }}/report_callback.py"`. Any ${{ }} inside a run: block is filled in before the shell reads the script. Set it as an env var instead (e.g. ACTION_PATH: ${{ github.action_path }}) and use "$ACTION_PATH/report_callback.py", or use the runner-provided "$GITHUB_ACTION_PATH".

Locations:

- `action.yml:224`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection

**Notes:**

Pinned actions/github-script@v9 to 3a2844b7e9c422d3c10d287c895573f7108da1b3 (# v9). Replaced the inline ${{ github.action_path }} in the bash run: with the runner-provided "$GITHUB_ACTION_PATH".

