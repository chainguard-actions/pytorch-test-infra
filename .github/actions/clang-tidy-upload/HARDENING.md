<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261027-001733** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts ${{ inputs.platform }} and ${{ inputs.version }} straight into the run: script, e.g. `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. Move them into env: variables and use them double-quoted.

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These uses: references point to tags, not full commit SHAs: aws-actions/configure-aws-credentials@v4 (line 37), seemethere/upload-artifact-s3@v5 (lines 45, 54), actions/upload-artifact@v6 (lines 64, 72).

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

I fixed all findings in hardened/action/action.yml and did not run the action afterwards.

- **Script injection:** in the 'Check if binaries have changed' step, inputs.platform and inputs.version now go through the step's env: block as INPUT_PLATFORM and INPUT_VERSION. The script uses them inside the double-quoted --s3-key strings. This covers the script-injection finding and all four static-inline-injection findings.
- **Pinned actions:** each uses: reference now points to the full commit SHA, with the tag kept as a comment:
  - aws-actions/configure-aws-credentials@7474bc4690e29a8392af63c5b98e7449536d5c3a # v4
  - seemethere/upload-artifact-s3@baba72d0712b404f646cebe0730933554ebce96a # v5 (both steps)
  - actions/upload-artifact@b7c566a772e6b6bfb58ed0dc250532a479d7789f # v6 (both steps)

The SHAs came from lookup_action_sha. Nothing else in the file was changed.

