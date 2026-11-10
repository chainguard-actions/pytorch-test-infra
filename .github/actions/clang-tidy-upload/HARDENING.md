<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261109-192709** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) is violated. The 'Check if binaries have changed' run: block puts ${{ inputs.platform }} and ${{ inputs.version }} directly into the shell script: `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. To fix this, pass the inputs through env: variables (e.g. PLATFORM and VERSION) and reference them double-quoted as "$PLATFORM/$VERSION/clang-tidy".

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These composite steps reference actions by mutable tag instead of a full 40-character commit SHA: `uses: aws-actions/configure-aws-credentials@v4`, `uses: seemethere/upload-artifact-s3@v5` (twice) and `uses: actions/upload-artifact@v6` (twice).

Locations:

- `action.yml:36`
- `action.yml:43`
- `action.yml:52`
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

In the 'Check if binaries have changed' step, inputs.platform and inputs.version are now passed through env: as PLATFORM and VERSION, and the script uses them double-quoted ("$PLATFORM/$VERSION/clang-tidy" and the clang-format equivalent). The five uses: references are pinned to full commit SHAs with the tag kept as a comment: aws-actions/configure-aws-credentials v4, seemethere/upload-artifact-s3 v5 (twice) and actions/upload-artifact v6 (twice). No tests were run.

