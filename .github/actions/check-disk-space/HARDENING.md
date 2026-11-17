<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: the env var MINIMUM_AVAILABLE_SPACE_IN_GB is set from inputs.minimum-available-space-in-gb, so the calling workflow controls it. It is expanded unquoted inside an arithmetic expansion: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash evaluates the expanded text as an arithmetic expression, and a value like `a[$(cmd)]` gets its array subscript expanded, which runs the command. Fix: check that the value is numeric first, e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`, then use the quoted form.

Locations:

- `action.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the step now checks MINIMUM_AVAILABLE_SPACE_IN_GB before doing anything else. It must match ^[0-9]+$, and if it doesn't, the step prints an error and exits 1. The arithmetic now refers to the variable by name ($((MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))) instead of pasting in its raw text with $VAR. A value like a[$(cmd)] can no longer run a command. Valid numbers, including the default of 6, behave as before. Nothing was run or tested.

