<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): data from the inputs is expanded unquoted. The step correctly passes inputs.docker-image and inputs.docker-registry through env vars (DOCKER_IMAGE, DOCKER_REGISTRY) and quotes them where they are passed in, e.g. `retry docker pull "${DOCKER_IMAGE}"` and `retry login "${DOCKER_REGISTRY}"`. But the helper `retry () { $*  || (sleep 1 && $*) || (sleep 2 && $*) }` expands them again with an unquoted `$*`. That splits the input-controlled values on whitespace and expands glob characters, so a crafted docker-image or docker-registry value (e.g. 'img --some-flag x') can add extra arguments to docker or aws. Fix: use "$@" instead of $* in retry.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Changed the retry() helper in action.yml so it runs its arguments as "$@" instead of the unquoted $*. DOCKER_IMAGE and DOCKER_REGISTRY now each reach the command as one argument, with no word splitting or glob expansion. Existing callers (retry login "$REG", retry docker pull "$IMG") behave the same.

