<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261029-163400** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): unquoted expansion of workflow-controlled data. The retry helper runs `$*  || (sleep 1 && $*) || (sleep 2 && $*)`, which re-expands its arguments without quotes. Those arguments come from the inputs docker-registry (via DOCKER_REGISTRY) and docker-image (via DOCKER_IMAGE), e.g. `retry docker pull "${DOCKER_IMAGE}"`. So even though the env vars are quoted at the call site, the shell splits the values on whitespace and expands globs again inside retry. Fix: use "$@" instead of $*.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Replaced unquoted $* with "$@" in the retry helper in action.yml, so arguments keep their boundaries and aren't split or glob-expanded again.

