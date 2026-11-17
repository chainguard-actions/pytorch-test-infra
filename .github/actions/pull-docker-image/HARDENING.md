<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): unquoted expansion of workflow-controlled data. The helper function `retry () { $*  || (sleep 1 && $*) || (sleep 2 && $*) }` expands its positional parameters unquoted. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, and both values come from inputs (inputs.docker-registry and inputs.docker-image). Quoting them at the call site does not help, because the unquoted $* splits them again on whitespace and expands glob characters. That lets an input add extra arguments to docker or aws. Fix: use "$@" instead of $*.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the retry helper now runs "$@" instead of $* in all three of its attempts. The registry and image inputs each stay a single argument. They are no longer split on whitespace or glob-expanded, so an input can't add extra arguments to the docker or aws commands. Every call passes one quoted value, so a normal input behaves exactly as before. I haven't run the action to check this.

