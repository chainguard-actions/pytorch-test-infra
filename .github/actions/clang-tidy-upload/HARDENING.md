<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261125-223308** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' run: block puts GitHub expressions straight into the shell script: `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. Move inputs.platform and inputs.version into env: variables and reference them double-quoted ("$PLATFORM", "$VERSION").

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These uses: references in action.yml point to version tags, not full commit SHAs: aws-actions/configure-aws-credentials@v4 (line 37), seemethere/upload-artifact-s3@v5 (lines 46, 55), actions/upload-artifact@v6 (lines 65, 73).

Locations:

- `action.yml:37`
- `action.yml:46`
- `action.yml:55`
- `action.yml:65`
- `action.yml:73`

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

In action.yml, the 'Check if binaries have changed' step now takes inputs.platform and inputs.version from env: as PLATFORM and VERSION, and the run: block uses them double-quoted ("$PLATFORM/$VERSION/clang-tidy" and "$PLATFORM/$VERSION/clang-format"). All uses: references are now pinned to full commit SHAs, looked up with lookup_action_sha, with the original tag kept as a comment: aws-actions/configure-aws-credentials (v4), seemethere/upload-artifact-s3 (v5, both steps) and actions/upload-artifact (v6, both steps). I haven't run the action or the analysis again to confirm the findings are cleared.

