<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261125-223308** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the env var MINIMUM_AVAILABLE_SPACE_IN_GB comes from inputs.minimum-available-space-in-gb, so the calling workflow controls it. It is expanded unquoted inside bash arithmetic: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash evaluates the value as an arithmetic expression, so a crafted value such as `a[$(cmd)]` runs a command. Check that the value is a whole number first (e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`), and quote the expansion.

Locations:

- `action.yml:29`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the script now checks that MINIMUM_AVAILABLE_SPACE_IN_GB matches ^[0-9]+$ at the top, outside the check_disk_space function and its subshell. If the value is not a whole number, the step exits 1 before any arithmetic runs. The expansion inside $(( )) is now double-quoted. Valid whole-number values behave exactly as before; a non-integer value fails the step with a clear error message. Not tested by running the action.

