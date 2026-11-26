<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261125-223308** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: in the 'Pull Docker image' step, the retry() helper expands its arguments unquoted: `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, and both values come from inputs (inputs.docker-registry, inputs.docker-image). The bare `$*` throws away the caller's quoting, so the shell word-splits and glob-expands these values and the command line is rebuilt from the pieces. A value containing spaces can add extra arguments to `docker pull` or `docker login`. Fix: change it to `"$@" || (sleep 1 && "$@") || (sleep 2 && "$@")`.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the retry() helper now runs its arguments as "$@" instead of a bare $*. The caller's quoting is kept, so the docker-registry and docker-image values reach docker as single arguments and are no longer split or glob-expanded.

