<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261118-220128** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the env var MINIMUM_AVAILABLE_SPACE_IN_GB comes from inputs.minimum-available-space-in-gb, and it is expanded unquoted inside a bash arithmetic expansion: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash arithmetic evaluates the expanded text, so a value such as `a[$(cmd)]` runs a command. Check the input is purely numeric before using it (e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`) and quote the expansion.

Locations:

- `action.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the step now checks that MINIMUM_AVAILABLE_SPACE_IN_GB matches ^[0-9]+$ before doing any math with it, and exits 1 if it doesn't. The arithmetic line now names the variable inside the expression and the result is quoted: "$(( MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024 ))". Inside the arithmetic, bash evaluates that variable's contents as an expression, so the digits-only check is what actually stops a command from running. Valid integer inputs, including the default 6, give the same result as before. Nothing was run or tested.

