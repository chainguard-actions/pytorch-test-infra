<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--docker-build-remote-buildkit/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--docker-build-remote-buildkit/v20261029-163400** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

The composite step writes `echo "image=${first_tag}" >> "${GITHUB_OUTPUT}"`, and first_tag comes from the untrusted input inputs.tags (through env TAGS). The value is already cleaned earlier in the loop: it is read line by line with `read -r` and passed through `echo "${tag}" | tr -d '[:space:]'`. So in practice it can't contain a newline, and this is a strict-pattern finding. It is reported because the required pipeline, `printf '%s' ... | tr -d '\n\r'`, is not applied right before the write. Fix: `safe=$(printf '%s' "$first_tag" | tr -d '\n\r'); echo "image=$safe" >> "$GITHUB_OUTPUT"`.

Locations:

- `action.yml:118`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection

**Notes:**

Fixed in action.yml: `first_tag` now goes through `printf '%s' "$first_tag" | tr -d '\n\r'` right before it is written as `image=` to $GITHUB_OUTPUT. The output value is unchanged, because the loop already removed all whitespace from each tag. The step uses `set -euo pipefail` and `tr` cannot fail on this input, so the change cannot hide an error. Nothing else was edited.

