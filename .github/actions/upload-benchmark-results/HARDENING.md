<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose `uses:` refs point at a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-uv@main` (line 31) and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main` (line 115). The second step is passed `inputs.github-token`. Pin both to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

I pinned both pytorch/test-infra sub-action references in action.yml (setup-uv and get-workflow-job-id) to commit 6f7274a0eff04dd4f8ada574e4e144610cece2c8, with a '# main' comment to show the original ref. I used the request's upstream_commit rather than looking up the SHA. It is a real commit in pytorch/test-infra, and it is the one this version was built from, so the sub-actions match the rest of the action instead of the current tip of main. Nothing else was changed and nothing was run to test it.

