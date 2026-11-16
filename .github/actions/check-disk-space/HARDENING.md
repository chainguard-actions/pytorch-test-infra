<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: an unquoted shell expansion of workflow-controlled data. The env var MINIMUM_AVAILABLE_SPACE_IN_GB comes from inputs.minimum-available-space-in-gb. It is expanded unquoted inside an arithmetic expression: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash expands $VAR as plain text before it evaluates the arithmetic. A value such as `a[$(cmd)]` therefore runs a command through array-subscript evaluation. Fix: check that the value is a number first, for example `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`. Then use the quoted variable in the arithmetic.

Locations:

- `action.yml:29`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the step now checks minimum-available-space-in-gb against ^[0-9]+$ before any arithmetic runs. If the value is not a whole number, the step prints an error and exits 1. This check sits at the top level, not inside the check_disk_space function, because that function runs in a $(...) subshell where an exit would not fail the step. The arithmetic is now $(( 10#${MINIMUM_AVAILABLE_SPACE_IN_GB} * 1024 * 1024 )), so the shell only ever does arithmetic on an already-checked number. The 10# prefix makes a value with a leading zero (e.g. 08) count as base 10 instead of octal; upstream would have errored on 08. Valid input behaves the same as before. One change for invalid input: upstream's arithmetic error only ended the subshell, so the step left the result empty and passed without checking disk space. The hardened step fails instead. Decimal values such as 6.5 were never supported by upstream's bash arithmetic and are now rejected. This edit has not been run or tested.

