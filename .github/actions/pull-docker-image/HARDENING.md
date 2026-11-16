<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261021-234439** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: an unquoted shell expansion of workflow-controlled data. The helper `retry () { $*  || (sleep 1 && $*) || (sleep 2 && $*) }` expands its arguments with an unquoted `$*`. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, and both values come from inputs (inputs.docker-registry and inputs.docker-image). Quoting at the call site does not help, because `$*` splits the values on whitespace again and expands globs. A caller can therefore pass extra arguments or options to `docker pull` and `docker login`, e.g. docker-image='img --platform x' or a glob. Fix: use "$@" in place of $*.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Replaced unquoted $* with "$@" in the retry helper in action.yml so registry/image inputs are passed as single arguments without word splitting or globbing.

