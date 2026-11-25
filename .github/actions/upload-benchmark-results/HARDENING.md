<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261119-192116** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by the mutable branch name @main instead of a full 40-character commit SHA: (1) 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31), (2) 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 122). Pin each one to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:122`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

I pinned both pytorch/test-infra sub-action references in action.yml (setup-uv on line 31 and get-workflow-job-id on line 122) to commit 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4, with a '# main' comment to show the original ref. This is the upstream commit this mirror version was built from, so both sub-actions now come from the same code as the main action. I confirmed with lookup_action_sha that the commit exists in pytorch/test-infra. Nothing has been run or re-scanned since the edit.

