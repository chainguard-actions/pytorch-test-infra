<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-uv@main` (line 31) and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main` (line 115). Whoever controls the main branch of pytorch/test-infra can change the code these steps run. Pin both to a full commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id in action.yml (lines 31 and 115) to commit 2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f instead of @main. That is the upstream commit this version was built from, and lookup_action_sha confirmed it exists. Each line keeps a '# main' comment so it's clear which branch was pinned. Nothing was run to test the change.

