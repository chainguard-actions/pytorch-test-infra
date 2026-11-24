<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261123-205410** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts `${{ inputs.platform }}` and `${{ inputs.version }}` straight into the run: script. Offending lines: `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. Fix: pass these through env: variables (e.g. PLATFORM, VERSION) and reference them double-quoted in the script.

Locations:

- `action.yml:28`
- `action.yml:31`

### unpinned-uses (severity: high)

Some uses: refs point to a tag instead of a full commit SHA: `aws-actions/configure-aws-credentials@v4` (line 35), `seemethere/upload-artifact-s3@v5` (lines 44, 53), `actions/upload-artifact@v6` (lines 62, 70).

Locations:

- `action.yml:35`
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

I moved `inputs.platform` and `inputs.version` out of the run: script and into the step's env: block as PLATFORM and VERSION. The script now uses them double-quoted in the --s3-key arguments. I pinned all five uses: refs to full commit SHAs found with lookup_action_sha, keeping the tag in a trailing comment: aws-actions/configure-aws-credentials v4, seemethere/upload-artifact-s3 v5 (2 places) and actions/upload-artifact v6 (2 places). The `${{ }}` expressions left in with:/if: fields are not shell contexts, so I didn't change them. Nothing was run or tested after the edits.

