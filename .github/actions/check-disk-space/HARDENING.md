<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the input-derived env var MINIMUM_AVAILABLE_SPACE_IN_GB (from inputs.minimum-available-space-in-gb) is expanded unquoted inside bash arithmetic: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash expands the text first and then evaluates the result as an arithmetic expression. A value such as `a[$(cmd)]` makes bash run command substitution during evaluation, so this can run commands. Check that the value is numeric before using it, for example `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`, and then reference the variable as `$((MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`.

Locations:

- `action.yml:29`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the step now checks that MINIMUM_AVAILABLE_SPACE_IN_GB contains only digits (^[0-9]+$) and exits 1 otherwise. The check runs at the top of the step, outside check_disk_space: that function is called inside $(...), so an exit there would only end the subshell and the step would carry on. The arithmetic now names the variable instead of expanding it first: $((MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024)). Not tested by running it. Behaviour change: a decimal value such as 6.5 now fails the check with a clear message. It already failed upstream as an arithmetic error, but upstream ignored that error and kept going.

