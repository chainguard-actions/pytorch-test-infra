<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): unquoted expansion of workflow-controlled data. The retry helper runs its arguments as `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, and both values come from inputs (inputs.docker-registry / inputs.docker-image). Quoting at the call site does not help, because the unquoted $* splits each value on whitespace again and expands globs. A crafted input can therefore pass extra arguments or flags to docker/aws. Fix: use "$@" in place of $* (e.g. `"$@" || (sleep 1 && "$@") || (sleep 2 && "$@")`).

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the retry helper now runs its arguments as "$@" instead of the unquoted $*. Before, the shell split docker-registry and docker-image on whitespace and expanded globs, so a crafted input could add extra arguments or flags to aws/docker. Now each value reaches the command as one argument. Nothing else changed.

