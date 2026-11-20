<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261119-192116** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts inputs.platform and inputs.version straight into the run: script, e.g. `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` (line 29) and the same pattern for clang-format (line 32). The values are substituted into the script text before the shell runs it, so input that contains quotes or shell metacharacters can inject commands. Fix: pass them through env: (e.g. PLATFORM, VERSION) and reference "$PLATFORM"/"$VERSION" in double quotes.

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These composite steps use tag refs instead of full commit SHAs: `uses: aws-actions/configure-aws-credentials@v4` (line 37), `uses: seemethere/upload-artifact-s3@v5` (lines 46, 55), `uses: actions/upload-artifact@v6` (lines 65, 73).

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

Both script-injection findings and the unpinned-uses finding are fixed in action.yml. I haven't run the action to test the change.

- **Injection:** in the 'Check if binaries have changed' step, inputs.platform and inputs.version now go through the step's env: block as PLATFORM and VERSION. The script refers to them as "$PLATFORM/$VERSION/..." in double quotes, so input values can no longer become shell code.
- **Pinned actions:** each of these now uses a full commit SHA, found with the lookup tool, with the original tag kept as a comment:
  - aws-actions/configure-aws-credentials v4 → 7474bc4690e29a8392af63c5b98e7449536d5c3a
  - seemethere/upload-artifact-s3 v5 → baba72d0712b404f646cebe0730933554ebce96a (2 places)
  - actions/upload-artifact v6 → b7c566a772e6b6bfb58ed0dc250532a479d7789f (2 places)

The expressions in the `with:` inputs of these steps are unchanged: they are passed as action inputs, not run by a shell, so they can't inject commands.

