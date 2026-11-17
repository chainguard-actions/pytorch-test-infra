<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261029-163400** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: the env var MINIMUM_AVAILABLE_SPACE_IN_GB holds the workflow-controlled input inputs.minimum-available-space-in-gb, and the script expands it unquoted inside an arithmetic expansion: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash arithmetic evaluates the expanded text as an expression. That includes array subscripts such as `a[$(cmd)]`, so a crafted input can run commands. Fix: check that the value is numeric before using it, e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`, then use the quoted expansion.

Locations:

- `action.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

I fixed the script-injection finding in action.yml. The script now checks MINIMUM_AVAILABLE_SPACE_IN_GB before doing anything else. It must be a non-negative integer (^[0-9]+$), otherwise the step exits with an error. I put the check at the top of the script because check_disk_space runs in a subshell via $(...), so an exit 1 inside that function would not fail the step. The arithmetic now reads $(( 10#${MINIMUM_AVAILABLE_SPACE_IN_GB} * 1024 * 1024 )). The 10# prefix makes bash read a value with leading zeros (e.g. 08) as base 10 instead of octal. The default of 6 and any other whole number work as before. A value like 6.5 now fails at the check rather than with a bash arithmetic error; bash arithmetic never handled decimals anyway. I haven't run the action to test this.

