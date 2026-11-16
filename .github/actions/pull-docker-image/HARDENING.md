<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: the retry() helper expands its arguments unquoted with `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. The function is called with workflow-controlled data (`retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, which come from inputs.docker-registry and inputs.docker-image). The unquoted `$*` re-splits those values on whitespace and expands globs, so the quoting at the call site is lost. Fix: use "$@" instead of $*.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Changed retry() in action.yml to expand its arguments as "$@" instead of unquoted $*, so DOCKER_REGISTRY/DOCKER_IMAGE keep their argument boundaries and are not re-split or globbed. Inputs were already passed via env.

