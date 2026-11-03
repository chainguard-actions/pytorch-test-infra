<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b), unquoted shell expansion of untrusted data. The env var MINIMUM_AVAILABLE_SPACE_IN_GB comes from inputs.minimum-available-space-in-gb, and the script expands it unquoted inside arithmetic expansion: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash arithmetic evaluates the expanded text as an expression. A value such as `a[$(cmd)]` would therefore run commands through array-subscript evaluation. Fix: quote the expansion and check that the value is numeric before using it, for example `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`.

Locations:

- `action.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Added a check at the top of the run script that exits with an error unless MINIMUM_AVAILABLE_SPACE_IN_GB is a non-negative integer (^[0-9]+$). This runs before check_disk_space, so the arithmetic expansion only gets digits. Changed the arithmetic to $(( 10#${MINIMUM_AVAILABLE_SPACE_IN_GB} * 1024 * 1024 )) so a value with a leading zero is read as decimal, not octal. Valid integer inputs, including the default 6, behave as before. Non-integer values such as 6.5 now fail with an error. Before this change, bash arithmetic rejected those values too.

