<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261109-192709** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): the env var MINIMUM_AVAILABLE_SPACE_IN_GB comes from inputs.minimum-available-space-in-gb, so the calling workflow controls it. It is expanded unquoted inside bash arithmetic: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash arithmetic evaluation runs array subscripts, so a value like `a[$(cmd)]` executes cmd. Fix: check that the value is a number first, e.g. `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`. Then use it in quoted or validated form.

Locations:

- `action.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In action.yml, the step now checks MINIMUM_AVAILABLE_SPACE_IN_GB before it does anything else: if the value is not made up only of digits (^[0-9]+$), the step stops with an error. The arithmetic line now reads $((10#$MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024)). The 10# makes bash read the number as base 10, so a value with leading zeros like 08 isn't treated as octal and rejected. Values upstream already handled (whole numbers, default 6) work the same as before. Decimals or negative numbers now stop the step with a clear error; upstream's arithmetic couldn't handle those either. I haven't run the action to test this.

