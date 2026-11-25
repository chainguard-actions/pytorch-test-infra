<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that uses a branch ref instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls the upstream `main` branch can change the code this step runs at any time. Pin it to a commit SHA.

Locations:

- `action.yml:96`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia@main to 6f7274a0eff04dd4f8ada574e4e144610cece2c8 (the upstream_commit this version was built from, same repository), keeping a '# main' comment.

