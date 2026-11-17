<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the step 'Get disk space usage and throw an error for low disk space' expands the input-derived env var MINIMUM_AVAILABLE_SPACE_IN_GB (from inputs.minimum-available-space-in-gb) unquoted inside bash arithmetic: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash evaluates the value inside the arithmetic expression as code. A value like `a[$(cmd)]` makes bash evaluate the array subscript, which runs the command substitution. Quoting the variable alone does not fix this because the arithmetic context still evaluates it. Check the value first, e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`, and only then use it in arithmetic.

Locations:

- `action.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

I fixed the script-injection finding in action.yml. The step now checks MINIMUM_AVAILABLE_SPACE_IN_GB against ^[0-9]+$ before any arithmetic and exits 1 with an error if it doesn't match. The arithmetic itself now uses $((10#${MINIMUM_AVAILABLE_SPACE_IN_GB} * 1024 * 1024)). The 10# makes bash read the number as decimal, so a value with a leading zero (e.g. 08) isn't treated as octal. Nothing was run to test this.

One behaviour change: if the input is set to something that isn't a whole number (e.g. 6.5 or an empty string), the step now fails. Upstream's arithmetic would have errored inside the subshell, leaving the result empty, so the step passed without checking disk space. The default (6) and other whole-number values work as before.

