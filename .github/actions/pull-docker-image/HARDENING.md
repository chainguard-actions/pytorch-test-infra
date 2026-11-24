<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261123-205410** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the `retry` helper expands its arguments unquoted: `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, and both values come from inputs.docker-registry and inputs.docker-image. The unquoted `$*` undoes the quoting at the call site, so these values are word-split and glob-expanded again. A value with spaces can therefore add extra arguments or options to `docker pull` / `docker login`. Fix: use "$@" instead of $* in all three places.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In the retry helper in action.yml, replaced the unquoted $* with "$@" in all three places. Arguments now pass through with their original word boundaries, so a value with spaces in the docker-registry or docker-image input can no longer add extra arguments to docker login or docker pull. The inputs were already passed in through env vars, and nothing else changed. I haven't run the action to check it.

