<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261021-234439** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the env var MINIMUM_AVAILABLE_SPACE_IN_GB holds the workflow-controlled input inputs.minimum-available-space-in-gb. It is expanded unquoted inside bash arithmetic: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash re-reads the expanded text as an arithmetic expression, so a value like `a[$(cmd)]` runs commands. Fix: check the value is numeric before using it, e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || { echo 'invalid input'; exit 1; }`. Then use `$(( MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024 ))`, which reads the variable by name instead of expanding it with $.

Locations:

- `action.yml:29`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the step now checks MINIMUM_AVAILABLE_SPACE_IN_GB against ^[0-9]+$ before anything else. The check sits at the top level of the script, not inside check_disk_space, because that function runs in a $(...) subshell and an exit there would not stop the step. A value that isn't a whole number now fails the step with an error message. The arithmetic now reads the variable by name, $(( MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024 )), instead of expanding it with $, so bash no longer re-parses the input as code. Nothing else changed. The edit has not been run or tested. One behaviour is the same as upstream: a value with a leading zero such as 08 is still read as octal, which makes the arithmetic fail.

