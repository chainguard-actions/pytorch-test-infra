<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--check-disk-space/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--check-disk-space/v20261119-192116** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (b): in the step 'Get disk space usage and throw an error for low disk space', the env var MINIMUM_AVAILABLE_SPACE_IN_GB holds the value of inputs.minimum-available-space-in-gb, so the calling workflow controls it. The script expands it unquoted inside shell arithmetic: `MINIMUM_AVAILABLE_SPACE_IN_KB=$(($MINIMUM_AVAILABLE_SPACE_IN_GB * 1024 * 1024))`. Bash evaluates arithmetic recursively, so a value like `a[$(cmd)]` runs a command through array-subscript evaluation. Fix: check the value against ^[0-9]+$ before the arithmetic, then quote the expansion.

Locations:

- `action.yml:29`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

action.yml: the step now checks MINIMUM_AVAILABLE_SPACE_IN_GB against ^[0-9]+$ before defining check_disk_space and exits 1 if it does not match. The arithmetic now uses the quoted expansion $(( "${MINIMUM_AVAILABLE_SPACE_IN_GB}" * 1024 * 1024 )). Nothing else changed. Not run or tested.

