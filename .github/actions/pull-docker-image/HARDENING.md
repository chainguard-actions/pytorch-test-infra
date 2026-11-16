<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261109-192709** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the retry() helper expands its arguments unquoted with `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, and both values come from inputs (inputs.docker-registry, inputs.docker-image). The unquoted $* splits those values on whitespace and expands globs, so an input can add extra arguments or options to the commands (for example `img --some-flag`). That undoes the quoting at the call site. Use "$@" instead.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Changed retry() in action.yml so it expands its arguments as "$@" instead of the unquoted $*. Each argument now reaches the command as one word, so a docker-image or docker-registry value can't be split into extra arguments or options. The callers pass single values, so they work as before.

