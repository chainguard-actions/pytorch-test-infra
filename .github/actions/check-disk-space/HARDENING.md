<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261103-202628** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: the workflow-controlled input `inputs.minimum-available-space-in-gb` is passed in through the env var MINIMUM_AVAILABLE_SPACE_IN_GB and expanded unquoted inside bash arithmetic: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash evaluates arithmetic expressions, so a value such as `a[$(cmd)]` runs a command. Quoting the variable does not help inside $(( )). Check the value against an integer-only pattern first (e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`) before using it in arithmetic.

Locations:

- `action.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Added an integer-only check (^[0-9]+$) on MINIMUM_AVAILABLE_SPACE_IN_GB at the top level of the step, before check_disk_space runs and before the value reaches bash arithmetic. If the value isn't an integer, the step prints an error and exits 1. The default of 6 and any other non-negative whole number behave as before.

