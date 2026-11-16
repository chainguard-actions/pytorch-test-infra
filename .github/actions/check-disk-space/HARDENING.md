<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261029-163400** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: an unquoted shell expansion of workflow-controlled data. The env var MINIMUM_AVAILABLE_SPACE_IN_GB comes from inputs.minimum-available-space-in-gb and is expanded unquoted inside a bash arithmetic expansion: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash evaluates the expanded text as an arithmetic expression. A value such as `a[$(cmd)]` makes bash run the command substitution, so a caller-supplied input can execute arbitrary commands. Fix: check that the value is an integer before using it (e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`), then reference it inside the arithmetic without the `$` prefix or quoted.

Locations:

- `action.yml:29`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

action.yml now checks MINIMUM_AVAILABLE_SPACE_IN_GB before doing any arithmetic with it. It must match ^[0-9]+$ or the step exits with an error. The arithmetic now uses the bare variable name, MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024, with no $ in front. An empty value is set to 0. Upstream's arithmetic failed on an empty value and the check passed silently, so 0 gives the same outcome (it always passes). Decimals and any non-integer text now stop the step with an error. Nothing was run to test this.

