<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261118-220128** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the 'Pull Docker image' step, the retry() helper expands its arguments unquoted: `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. The arguments include workflow-controlled data (DOCKER_REGISTRY from inputs.docker-registry, DOCKER_IMAGE from inputs.docker-image, called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`). The values get split on whitespace and glob-expanded again after the call site quoted them. Use "$@" instead of $*.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the retry() helper used to expand its arguments as an unquoted $* in all three attempts. It now uses "$@", so each argument reaches the command as the same single word the caller passed. That covers the registry and image values coming from the inputs, which now get no extra word splitting or glob expansion. Every call site passes simple arguments (a function name or a command, then one quoted value), so the action behaves the same for normal inputs. Nothing was run to test this.

