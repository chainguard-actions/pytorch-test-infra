<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20260922-155642** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' run: block puts inputs.platform and inputs.version straight into the shell script, e.g. `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. Fix: pass them through env: variables (e.g. PLATFORM, VERSION) and use "$PLATFORM/$VERSION/..." in double quotes.

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These uses: references point to version tags, not full 40-character commit SHAs: aws-actions/configure-aws-credentials@v4 (line 37), seemethere/upload-artifact-s3@v5 (lines 45, 54), actions/upload-artifact@v6 (lines 64, 72).

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

I fixed both findings in action.yml.

- **Script injection:** in the 'Check if binaries have changed' step, inputs.platform and inputs.version now go through the step's env: block as PLATFORM and VERSION. The two s3-key arguments use "$PLATFORM/$VERSION/..." in double quotes, so the paths are the same as before but the inputs can't run as shell code.
- **Unpinned actions:** all five uses: references now point to full commit SHAs, each with its original tag kept in a comment. The SHAs came from lookup_action_sha:
  - aws-actions/configure-aws-credentials v4: 7474bc4690e29a8392af63c5b98e7449536d5c3a
  - seemethere/upload-artifact-s3 v5 (both steps): baba72d0712b404f646cebe0730933554ebce96a
  - actions/upload-artifact v6 (both steps): b7c566a772e6b6bfb58ed0dc250532a479d7789f

The remaining ${{ }} expressions are in with: values and an if:, not in shell scripts, so they can't be injected and I left them alone. Nothing has been run to test the changes.

