<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-192709** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by the mutable branch `@main` instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-uv@main` (line 31) and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main` (line 115). Whoever controls that branch can change the code these steps run. Pin each one to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id in action.yml to commit 0569df511711f70601c984fe3a93dac324afc9ce, replacing @main. That is the upstream commit this version was built from, and lookup_action_sha confirmed it exists in pytorch/test-infra. Each line keeps a '# v20261109-192709' comment. Pinning to this commit rather than the current main head keeps the two sub-actions at the same version as the action's own scripts. I didn't run anything to test it.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

Fixed the 'Install dependencies' step in action.yml. It now removes newline and carriage-return characters from ${RUNNER_TEMP}/benchmark-upload-venv before writing VIRTUAL_ENV to "$GITHUB_ENV", and $GITHUB_ENV is now quoted. The 'export VIRTUAL_ENV' line and the venv path are unchanged. I also made the same change to the DEVICE_TYPE write in 'Get device type', because that value comes from command output and would likely be flagged next. In 'Get device name' I only quoted "$GITHUB_ENV"; DEVICE_NAME is always one of a fixed set of words, so it didn't need cleaning. No other behaviour changed. Nothing was run to test these edits.

