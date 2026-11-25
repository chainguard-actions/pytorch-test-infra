<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261125-022556** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the env var MINIMUM_AVAILABLE_SPACE_IN_GB holds the value of inputs.minimum-available-space-in-gb, and the script expands it unquoted inside shell arithmetic: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash evaluates the expanded text as an arithmetic expression, so a value like `a[$(cmd)]` runs a command through array-subscript evaluation. Check that the input contains only digits (e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`) before using it, and quote the expansion.

Locations:

- `action.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Added a digits-only check (^[0-9]+$) on MINIMUM_AVAILABLE_SPACE_IN_GB. It runs before the value is used and exits 1 on anything else. The arithmetic expansion is now quoted: $(( "${MINIMUM_AVAILABLE_SPACE_IN_GB}" * 1024 * 1024 )). The default of 6 and any other whole number behave exactly as before. Nothing was run or tested.

