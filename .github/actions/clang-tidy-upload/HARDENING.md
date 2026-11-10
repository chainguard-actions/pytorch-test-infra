<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261109-232755** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' run: block puts ${{ inputs.platform }} and ${{ inputs.version }} directly into the shell command, e.g. `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. Fix: pass them in through env: (for example PLATFORM and VERSION) and reference them as "${PLATFORM}/${VERSION}/clang-tidy".

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These uses: references point to mutable tags instead of 40-character commit SHAs: aws-actions/configure-aws-credentials@v4, seemethere/upload-artifact-s3@v5 (twice), actions/upload-artifact@v6 (twice).

Locations:

- `action.yml:37`
- `action.yml:44`
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

In the 'Check if binaries have changed' step, inputs.platform and inputs.version now go in through the step's env: block as PLATFORM and VERSION. The script uses them as "${PLATFORM}/${VERSION}/...". I pinned aws-actions/configure-aws-credentials@v4, seemethere/upload-artifact-s3@v5 (2 uses) and actions/upload-artifact@v6 (2 uses) to full commit SHAs found with lookup_action_sha, with the tag kept in a comment after each one. Inputs used in with: blocks were left as they were, because with: values are not run by a shell.

