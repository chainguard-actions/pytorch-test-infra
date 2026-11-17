<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--cross-repo-ci-relay-callback/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite step pins its action to a tag, not a full commit SHA: `uses: actions/github-script@v9`. Pin it to a 40-character commit SHA.

Locations:

- `action.yml:133`

### script-injection (severity: high)

Rule (a): a GitHub Actions expression is interpolated directly into a run: script in the 'Send callback to relay server' step: `run: python3 "${{ github.action_path }}/report_callback.py"`. Use the $GITHUB_ACTION_PATH env var instead, written as "$GITHUB_ACTION_PATH/report_callback.py".

Locations:

- `action.yml:189`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection

**Notes:**

In action.yml, I pinned actions/github-script@v9 to the commit SHA 3a2844b7e9c422d3c10d287c895573f7108da1b3, which lookup_action_sha returned for the v9 tag, and kept '# v9' as a comment. In the 'Send callback to relay server' step, the run: line now uses "$GITHUB_ACTION_PATH/report_callback.py" instead of the inline github.action_path expression. That step uses shell: bash, so the $VAR syntax is correct there. I did not run any tests; no other files changed.

