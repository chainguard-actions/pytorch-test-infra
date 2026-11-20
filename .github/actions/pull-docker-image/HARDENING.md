<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261119-192116** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): an unquoted expansion of workflow-controlled data. The retry helper runs `$*  || (sleep 1 && $*) || (sleep 2 && $*)` with $* unquoted. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`. Both values come from inputs.docker-registry and inputs.docker-image. Because $* is unquoted, the shell splits these values on whitespace and expands globs again, so a crafted input can add extra arguments to docker or aws, such as docker pull options. Use "$@" instead of $*.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Changed the retry helper in action.yml so it runs "$@" instead of an unquoted $*. Each argument now stays one word: the docker-registry and docker-image values are no longer split on spaces or expanded as globs. The callers already pass each one as a single quoted value, so normal use behaves the same. Not tested by running the action.

