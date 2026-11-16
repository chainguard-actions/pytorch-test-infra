<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261021-234439** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the step "Check if binaries have changed" puts GitHub expressions straight into its run: script: `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. The values are substituted into the script text before the shell runs, so the double quotes don't protect them. Fix: pass inputs.platform and inputs.version in through env: and use them as "$PLATFORM" / "$VERSION".

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These uses: references point at a mutable tag instead of a full 40-character commit SHA: aws-actions/configure-aws-credentials@v4, seemethere/upload-artifact-s3@v5 (used twice), actions/upload-artifact@v6 (used twice).

Locations:

- `action.yml:37`
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

In action.yml, the "Check if binaries have changed" step no longer puts inputs.platform or inputs.version straight into its run: script. Both now come in through the step's env: as PLATFORM and VERSION, and the script uses "$PLATFORM/$VERSION/..." inside double quotes. Pinned every uses: reference to a full commit SHA and kept the tag as a trailing comment: aws-actions/configure-aws-credentials@7474bc4690e29a8392af63c5b98e7449536d5c3a (v4), seemethere/upload-artifact-s3@baba72d0712b404f646cebe0730933554ebce96a (v5, 2 places), actions/upload-artifact@b7c566a772e6b6bfb58ed0dc250532a479d7789f (v6, 2 places). Nothing was run to test the changes. The ${{ }} expressions left in with: and if: aren't shell scripts, so I didn't change them.

