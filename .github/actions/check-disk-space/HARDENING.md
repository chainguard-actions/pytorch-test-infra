<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the composite step 'Get disk space usage and throw an error for low disk space', the env var MINIMUM_AVAILABLE_SPACE_IN_GB comes from inputs.minimum-available-space-in-gb and is expanded without quotes inside a bash arithmetic expression: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash arithmetic evaluates the value it is given, so input such as `a[$(cmd)]` can run commands. Check that the value is a whole number first (e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`), then do the arithmetic.

Locations:

- `action.yml:29`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the step now checks that MINIMUM_AVAILABLE_SPACE_IN_GB matches ^[0-9]+$ at the top level, before any arithmetic, and fails the step with an error if it doesn't. This stops values like 'a[$(cmd)]' from being evaluated. The arithmetic now uses the 10# prefix (base 10), so a value with leading zeros such as 08 isn't read as octal. Upstream only works with whole numbers, so valid inputs behave as before. One behaviour change: a malformed value used to cause an arithmetic error inside the check's subshell and the step could still pass; now it fails clearly. Nothing was run to test this.

