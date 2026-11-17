<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261109-192709** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): an unquoted shell expansion of workflow-controlled data. MINIMUM_AVAILABLE_SPACE_IN_GB comes from the input inputs.minimum-available-space-in-gb through env:, and it is expanded unquoted inside a bash arithmetic expansion: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash evaluates the expanded text as an arithmetic expression. A value such as `a[$(cmd)]` makes bash run the command substitution inside the array subscript, so the input can run commands. Fix: check the input first, e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`, and then use the quoted form `$(( "$MINIMUM_AVAILABLE_SPACE_IN_GB" * 1024 * 1024 ))` or the bare name `$(( MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024 ))`.

Locations:

- `action.yml:29`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the input `minimum-available-space-in-gb` is now checked at the start of the step against ^[0-9]+$. If it is anything else, the step stops with exit 1 before any arithmetic runs. The arithmetic line now uses the bare variable name: $(( MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024 )). Using the bare name alone would not have closed the hole, since bash evaluates the variable's value again as an expression. The digits-only check is what stops it. Valid whole-number inputs, including the default of 6, behave as before.

