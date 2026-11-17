<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): unquoted expansion of workflow-controlled data. The `retry` helper in the 'Pull Docker image' step runs `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, and both values come from inputs (inputs.docker-registry and inputs.docker-image). Because `$*` is unquoted, those values are split on whitespace and glob-expanded again, which drops the quoting the caller added. An input with spaces can therefore add extra arguments to `docker pull` or `login`. Fix: use "$@" instead of $*.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the retry helper now runs its arguments as "$@" instead of the unquoted $*. The registry and image inputs now reach login and docker pull as one argument each, so the shell no longer splits them on spaces or expands them as globs. The retry behaviour is the same as before. I made no other changes, and I didn't run the action to test it.

