<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261118-220128** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' run step puts ${{ inputs.platform }} and ${{ inputs.version }} straight into the shell script: `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. Fix: pass the inputs in through env: variables and use them double-quoted ("$PLATFORM/$VERSION/clang-tidy").

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These composite steps point to tags instead of full commit SHAs: aws-actions/configure-aws-credentials@v4 (line 36), seemethere/upload-artifact-s3@v5 (lines 44, 53) and actions/upload-artifact@v6 (lines 62, 70).

Locations:

- `action.yml:36`
- `action.yml:44`
- `action.yml:53`
- `action.yml:62`
- `action.yml:70`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.platform }}" appears directly in run: block of step "Check if binaries have changed"; move to env: map

Locations:

- `action.yml:29`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.version }}" appears directly in run: block of step "Check if binaries have changed"; move to env: map

Locations:

- `action.yml:29`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.platform }}" appears directly in run: block of step "Check if binaries have changed"; move to env: map

Locations:

- `action.yml:32`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.version }}" appears directly in run: block of step "Check if binaries have changed"; move to env: map

Locations:

- `action.yml:32`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, static-inline-injection, unpinned-uses

**Notes:**

In hardened/action/action.yml, the 'Check if binaries have changed' step no longer puts inputs.platform and inputs.version straight into its shell script. They now go in through the step's env: block as PLATFORM and VERSION, and the script uses them double-quoted. I pinned the five tag references to full commit SHAs from lookup_action_sha, keeping the tag as a comment: aws-actions/configure-aws-credentials v4 (7474bc46…), seemethere/upload-artifact-s3 v5 (baba72d0…, two steps) and actions/upload-artifact v6 (b7c566a7…, two steps). Nothing has been run or tested.

