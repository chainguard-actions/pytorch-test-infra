<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261125-022556** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts expressions straight into its run: script: --s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy" and --s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format". The double quotes don't help because the values are substituted into the script before the shell sees it. To fix, pass inputs.platform and inputs.version through env: variables and use them double-quoted, e.g. "$PLATFORM/$VERSION/clang-tidy".

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

Some uses: references point to a mutable tag instead of a full commit SHA: aws-actions/configure-aws-credentials@v4 (line 37), seemethere/upload-artifact-s3@v5 (lines 45, 54) and actions/upload-artifact@v6 (lines 64, 72).

Locations:

- `action.yml:37`
- `action.yml:45`
- `action.yml:54`
- `action.yml:64`
- `action.yml:72`

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

In action.yml, the 'Check if binaries have changed' step now reads inputs.platform and inputs.version from env: variables (PLATFORM, VERSION) and uses them double-quoted in the --s3-key arguments, so they no longer appear inside the run: script. Every uses: reference is now pinned to the full commit SHA its tag pointed to when I looked it up, with the tag kept in a comment: aws-actions/configure-aws-credentials v4 → 7474bc46…, seemethere/upload-artifact-s3 v5 → baba72d0… and actions/upload-artifact v6 → b7c566a7…. The expressions in with: blocks were left as they are because they are not run by a shell. Nothing was run to test these changes.

