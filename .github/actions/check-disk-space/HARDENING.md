<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: an env var holding workflow-controlled data is expanded unquoted. The line is `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. MINIMUM_AVAILABLE_SPACE_IN_GB comes from inputs.minimum-available-space-in-gb. Because `$VAR` inside `$(( ))` is expanded as text before the arithmetic is evaluated, a crafted input such as `a[$(cmd)]` makes bash evaluate the array subscript and run the command. Fix: check the value is numeric first (e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`), then use it as a quoted or bare variable name in the arithmetic.

Locations:

- `action.yml:29`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

action.yml: the step now checks MINIMUM_AVAILABLE_SPACE_IN_GB against ^[0-9]+$ at the top level before anything else runs, and exits 1 if it is not a number. The check sits outside check_disk_space because that function runs inside $(...), where an exit would only end the subshell and not the step. The arithmetic now names the variable bare ($((MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))), so the input text is no longer pasted into the expression. No test run; checked by reading the file. For whole numbers the result is the same as upstream.

