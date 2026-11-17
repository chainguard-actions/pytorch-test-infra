<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261109-192709** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' run: block puts ${{ inputs.platform }} and ${{ inputs.version }} straight into the shell script, e.g. `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. Fix: move both inputs into env: variables and use them as "$PLATFORM" and "$VERSION" in double quotes.

Locations:

- `action.yml:28`
- `action.yml:31`

### unpinned-uses (severity: high)

These uses: references point to a mutable tag instead of a full 40-character commit SHA: `uses: aws-actions/configure-aws-credentials@v4` (line 36), `uses: seemethere/upload-artifact-s3@v5` (lines 44, 53) and `uses: actions/upload-artifact@v6` (lines 63, 71).

Locations:

- `action.yml:36`
- `action.yml:44`
- `action.yml:53`
- `action.yml:63`
- `action.yml:71`

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

I moved inputs.platform and inputs.version out of the 'Check if binaries have changed' script and into the step's env: block as PLATFORM and VERSION. The script now reads them in double quotes. I also pinned all five uses: lines to full commit SHAs and kept the tag as a trailing comment: configure-aws-credentials v4, upload-artifact-s3 v5 (twice) and upload-artifact v6 (twice). The ${{ }} expressions left in with:/if: fields are not run by a shell, so I didn't change them. Nothing was run to test these edits.

