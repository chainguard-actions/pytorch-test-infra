<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261021-234439** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: an unquoted shell variable expands untrusted data. The env var MINIMUM_AVAILABLE_SPACE_IN_GB comes from inputs.minimum-available-space-in-gb and is expanded unquoted inside bash arithmetic: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash evaluates arithmetic recursively, so a value like `a[$(cmd)]` can run commands through the array subscript. Fix: check that the value is numeric before using it (e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`) and quote the reference.

Locations:

- `action.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

The step now checks minimum-available-space-in-gb before doing any arithmetic. If the value isn't a non-negative integer (^[0-9]+$), the step prints an error and exits with status 1. This check runs in the top-level shell rather than inside the check_disk_space function, which is called through $(...) and so runs in a subshell. Because the value is now known to contain only digits, the arithmetic can't run commands. The expansion now reads 10#${MINIMUM_AVAILABLE_SPACE_IN_GB} so a number with leading zeros is read as decimal rather than octal. Valid values give the same result as before, including the default of 6. One behaviour change: a non-integer value such as 6.5 now fails with a clear error, where before it hit an arithmetic error. Upstream's integer-only arithmetic couldn't handle decimals either. I haven't run the action to test this.

