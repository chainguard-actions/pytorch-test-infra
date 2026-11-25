<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261125-022556** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation, unquoted expansion of workflow-controlled data. The retry helper has the line `$*  || (sleep 1 && $*) || (sleep 2 && $*)`, which expands its arguments unquoted. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, so the input values inputs.docker-registry and inputs.docker-image are split on whitespace and glob-expanded again, even though they are quoted at the call site. A value containing spaces would inject extra arguments into `docker login` or `docker pull` (for example option flags). Fix: use `"$@" || (sleep 1 && "$@") || (sleep 2 && "$@")`.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the retry helper now runs its arguments as "$@" instead of an unquoted $*. Each argument stays one word, so the docker-image and docker-registry inputs are no longer split on spaces or expanded as globs. Normal image and registry values behave exactly as before. Not tested by running the action.

