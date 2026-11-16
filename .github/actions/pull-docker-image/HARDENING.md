<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261029-163400** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in action.yml, the retry helper expands its arguments unquoted: `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, so the input values (inputs.docker-registry / inputs.docker-image) are passed to the helper quoted but then expanded unquoted. The shell then splits them on whitespace and expands globs. A crafted value can add extra arguments or options to `docker pull` and `docker login`. Fix: use "$@" instead of $*.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In the retry helper in action.yml, I changed the unquoted $* to "$@" in all three attempts. Before this, a value containing spaces or glob characters could add extra arguments to `docker login` or `docker pull`; now each argument passes through as a single word. Both callers already passed single quoted values, so a normal registry or image name behaves the same as before. No other changes were needed. The inputs were already passed through env:. Nothing was run to test the change.

