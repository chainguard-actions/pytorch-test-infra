<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261103-202628** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts GitHub expressions straight into the run: script: `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. Fix: pass the inputs through env: variables (for example PLATFORM and VERSION) and refer to them as "$PLATFORM" and "$VERSION" in double quotes.

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

action.yml has uses: refs pinned to tags instead of full commit SHAs: aws-actions/configure-aws-credentials@v4 (line 36), seemethere/upload-artifact-s3@v5 (lines 45, 54) and actions/upload-artifact@v6 (lines 63, 71).

Locations:

- `action.yml:36`
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

I made two changes to action.yml, and haven't run or tested the result.

1. Script injection: the 'Check if binaries have changed' step used to put `${{ inputs.platform }}` and `${{ inputs.version }}` straight into its shell script. Those values now go in through the step's env: block as PLATFORM and VERSION, and the two `--s3-key` arguments use them in double quotes ("$PLATFORM/$VERSION/clang-tidy" and "$PLATFORM/$VERSION/clang-format"). The script runs the same commands as before.

2. Unpinned actions: every uses: reference now points to a full commit SHA, with the original tag kept as a comment:
- aws-actions/configure-aws-credentials v4 → 7474bc4690e29a8392af63c5b98e7449536d5c3a
- seemethere/upload-artifact-s3 v5 → baba72d0712b404f646cebe0730933554ebce96a (2 places)
- actions/upload-artifact v6 → b7c566a772e6b6bfb58ed0dc250532a479d7789f (2 places)

The inputs are still written as expressions in the with: and if: fields of the other steps. That's expected: those fields aren't run by a shell, so no rule asks for a change there.

