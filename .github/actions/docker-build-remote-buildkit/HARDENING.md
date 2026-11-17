<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--docker-build-remote-buildkit/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--docker-build-remote-buildkit/v20261029-163400** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

The composite step 'Build and push with remote BuildKit' writes `echo "image=${first_tag}" >> "${GITHUB_OUTPUT}"`. `first_tag` comes from the untrusted `inputs.tags` (passed in as env TAGS). The value is read one line at a time and stripped with `tr -d '[:space:]'` higher up in the loop, so in practice it cannot hold newlines and the real risk is low. Still, the required sanitization pipeline (`printf '%s' "$first_tag" | tr -d '\n\r'`) does not run immediately before the write, so this fails the check as written. Fix: `safe=$(printf '%s' "$first_tag" | tr -d '\n\r'); echo "image=$safe" >> "$GITHUB_OUTPUT"`.

Locations:

- `action.yml:111`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection

**Notes:**

action.yml: first_tag now goes through printf '%s' | tr -d '\n\r' right before it is written to GITHUB_OUTPUT. Nothing else in the action changed.

