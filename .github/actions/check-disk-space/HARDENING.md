<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261123-205410** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the env var MINIMUM_AVAILABLE_SPACE_IN_GB comes from inputs.minimum-available-space-in-gb, so the calling workflow controls it. It is expanded unquoted inside bash arithmetic expansion: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash evaluates the expanded text as an arithmetic expression. A value such as `x[$(cmd)]` makes bash run the command substitution in the array subscript, so this is command injection. Fix: check that the value is a plain integer first, e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`, then compute.

Locations:

- `action.yml:29`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the step now checks that MINIMUM_AVAILABLE_SPACE_IN_GB is a plain non-negative integer (^[0-9]+$) before anything else uses it. If it is not, the step exits with an error. The check sits at the top level of the script, not inside check_disk_space: that function runs in a subshell under set +e, where an exit would not stop the step. The arithmetic now reads $((10#${MINIMUM_AVAILABLE_SPACE_IN_GB} * 1024 * 1024)). The 10# prefix makes bash read a value with a leading zero as decimal, not octal. Nothing was run or tested. The step now fails on values upstream accepted, such as a decimal like 6.5.

