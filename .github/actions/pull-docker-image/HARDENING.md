<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261021-234439** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): unquoted expansion of workflow-controlled data. The `retry` function in the 'Pull Docker image' step runs its arguments as `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, and both values come from inputs.docker-registry and inputs.docker-image. The unquoted `$*` re-splits those values on whitespace and expands glob characters, so the quoting at the call site no longer protects them. A crafted input can add extra arguments or flags to `docker pull`, `docker login` and `aws`. Fix: use "$@" instead of $*, for example `"$@" || (sleep 1 && "$@") || (sleep 2 && "$@")`.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the retry function now runs its command with "$@" instead of the unquoted $*. Each argument from the call site stays one word, so the registry and image inputs can no longer be split on spaces or expanded as globs. Nothing was run to test this. It doesn't change how the action behaves for normal single-word image and registry values.

