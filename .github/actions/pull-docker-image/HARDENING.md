<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: the retry() helper in the 'Pull Docker image' step runs its arguments as `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. The unquoted $* expands workflow-controlled data from inputs.docker-registry (via `retry login "${DOCKER_REGISTRY}"`) and inputs.docker-image (via `retry docker pull "${DOCKER_IMAGE}"`), so the quoting at the call sites is lost. The shell then splits these values on whitespace and expands glob characters, which means a crafted input can add extra arguments or options to `docker pull` or `docker login`. Fix: use "$@" instead of $* in all three places.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the retry() helper ran its arguments as an unquoted $*. I changed all three places to "$@", so the quoting at the call sites now holds and the registry and image inputs each reach docker login and docker pull as one argument. They are no longer split on spaces or expanded as glob patterns. The inputs were already passed in through env:, so nothing else needed to change. No tests were run.

