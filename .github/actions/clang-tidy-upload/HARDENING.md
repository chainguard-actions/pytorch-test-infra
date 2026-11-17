<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261021-234439** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts expressions straight into the run: script: `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. A value containing a double quote, $(...) or backticks can run commands in the shell. Fix: pass the inputs through env: vars (e.g. PLATFORM, VERSION) and write them double-quoted, as "${PLATFORM}/${VERSION}/clang-tidy".

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

action.yml has uses: references pinned to a tag, not a full 40-char commit SHA: aws-actions/configure-aws-credentials@v4 (line 37), seemethere/upload-artifact-s3@v5 (lines 45, 54), actions/upload-artifact@v6 (lines 63, 71).

Locations:

- `action.yml:37`
- `action.yml:45`
- `action.yml:54`
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

In action.yml, the 'Check if binaries have changed' step now takes inputs.platform and inputs.version through env: as PLATFORM and VERSION. The script uses them double-quoted, as "${PLATFORM}/${VERSION}/clang-tidy" and "${PLATFORM}/${VERSION}/clang-format". I pinned all five uses: lines to full commit SHAs from lookup_action_sha, with the original tag kept as a comment after each one. configure-aws-credentials v4 is now 7474bc4690e29a8392af63c5b98e7449536d5c3a, upload-artifact-s3 v5 (both steps) is baba72d0712b404f646cebe0730933554ebce96a, and upload-artifact v6 (both steps) is b7c566a772e6b6bfb58ed0dc250532a479d7789f. I haven't run the action or a new analysis pass to confirm the findings are cleared.

