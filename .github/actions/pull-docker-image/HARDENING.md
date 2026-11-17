<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--pull-docker-image/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--pull-docker-image/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the 'Pull Docker image' step, the retry helper expands its arguments unquoted: `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. It is called as `retry login "${DOCKER_REGISTRY}"` and `retry docker pull "${DOCKER_IMAGE}"`, and both values come from workflow inputs (inputs.docker-registry and inputs.docker-image). Because $* is unquoted, the shell splits these values on whitespace and expands globs again. An attacker can use this to inject extra arguments into `docker pull` or `login`, for example `--platform=...` or other flags. The quoting the caller added is lost. Fix: use "$@" instead of $*.

Locations:

- `action.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the retry helper now runs its command with "$@" instead of an unquoted $*. Each argument is passed through unchanged, so the image and registry values are no longer split on spaces or expanded as globs. The callers already pass a single quoted value each, so the action behaves the same for normal inputs. Not run or tested after the change.

