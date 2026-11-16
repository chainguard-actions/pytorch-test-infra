<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261103-202628** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b) violation: an unquoted shell expansion of workflow-controlled data. The env var MINIMUM_AVAILABLE_SPACE_IN_GB comes straight from inputs.minimum-available-space-in-gb. It is expanded unquoted inside an arithmetic expansion: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash does arithmetic evaluation on the expanded text, so a value like `a[$(id)]` runs a command through array-subscript evaluation. To fix it, first check that the value is a plain integer (for example `[[ "$MINIMUM_AVAILABLE_SPACE_IN_GB" =~ ^[0-9]+$ ]] || exit 1`). Then use the variable inside the arithmetic expansion without the `$` prefix or quoted.

Locations:

- `action.yml:29`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed the script-injection finding in action.yml. The minimum-available-space-in-gb input was dropped straight into a bash arithmetic expansion, where a crafted value could run a command. The script now checks the value at the top, before the check function runs. It stops with an error unless the value is a non-negative whole number matching ^[0-9]+$.

Two behaviour changes from upstream:
- An empty value now falls back to the default of 6. In upstream, an empty value broke the arithmetic inside a subshell, so the step passed without checking anything.
- Leading zeros are stripped, so a value like 08 isn't read as an octal number and rejected.

The arithmetic now names the variable without the $ prefix: $((MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024)). I haven't run the changed step.

