<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261112-155209** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): The 'Check if binaries have changed' run block puts ${{ inputs.platform }} and ${{ inputs.version }} straight into the shell script, e.g. `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. To fix it, pass the inputs through env: variables (e.g. PLATFORM, VERSION) and reference them double-quoted as "$PLATFORM/$VERSION/clang-tidy".

Locations:

- `action.yml:28`
- `action.yml:31`

### unpinned-uses (severity: high)

Composite steps reference actions by mutable tag instead of a 40-char commit SHA: `uses: aws-actions/configure-aws-credentials@v4`, `uses: seemethere/upload-artifact-s3@v5` (twice), `uses: actions/upload-artifact@v6` (twice).

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

Both findings are fixed in action.yml.

- **Script injection:** in the 'Check if binaries have changed' step, `inputs.platform` and `inputs.version` no longer go straight into the shell script. They are passed in through the step's `env:` block as PLATFORM and VERSION, and the script uses them double-quoted as "$PLATFORM/$VERSION/...".
- **Unpinned actions:** each `uses:` now points to a full commit SHA, with the original tag kept as a trailing comment. I looked up each SHA rather than guessing:
  - aws-actions/configure-aws-credentials v4: 7474bc4690e29a8392af63c5b98e7449536d5c3a
  - seemethere/upload-artifact-s3 v5 (both uses): baba72d0712b404f646cebe0730933554ebce96a
  - actions/upload-artifact v6 (both uses): b7c566a772e6b6bfb58ed0dc250532a479d7789f

I didn't run anything to test the changes. The remaining `${{ }}` expressions are inputs to other actions (`with:`) or `if:` conditions, not shell code, so I left them as they were.

