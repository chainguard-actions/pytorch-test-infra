<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261103-202628** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the `retry` helper expands its arguments unquoted with `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, and both values come from inputs (inputs.docker-registry and inputs.docker-image). The quoting at the call site is undone inside the helper, so whitespace and glob characters in the input are split and expanded again. That can add extra arguments or options to `docker pull` or `docker login`. Fix: change `$*` to "$@" so each argument stays intact.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the retry helper now runs its arguments as "$@" instead of unquoted $*. Before this, the quoting of the docker-image and docker-registry inputs was lost inside the helper, so whitespace or glob characters in them could add extra arguments or options to docker pull or docker login. Each argument now passes through intact. Callers are unchanged: the shell function `login` and the `docker` command still run the same way. No other changes; I didn't run the action to test it.

