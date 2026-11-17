<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the env var MINIMUM_AVAILABLE_SPACE_IN_GB holds the value of inputs.minimum-available-space-in-gb. It is expanded unquoted inside bash arithmetic on this line: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash evaluates array subscripts inside arithmetic, so an input such as `a[$(cmd)]` runs a command. Fix: check that the value is a whole number before using it, e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`. Then reference it quoted.

Locations:

- `action.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

action.yml now checks the minimum-available-space-in-gb input before using it. If the value isn't a whole number (^[0-9]+$), the step fails with an error message, so a value like a[$(cmd)] never reaches bash arithmetic. The check runs at the top level of the step, outside check_disk_space (whose output is captured into a variable), so the exit really stops the step. The variable is also quoted inside the arithmetic expansion now. Valid numeric inputs behave as before. I haven't run the action to test this.

