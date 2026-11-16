<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261029-163400** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts ${{ inputs.platform }} and ${{ inputs.version }} straight into the run: script, e.g. `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. The values are substituted into the script before the shell runs it, so a crafted input can break out of the quotes and run commands. Pass them through env: variables (e.g. PLATFORM, VERSION) and use "$PLATFORM/$VERSION/..." with double quotes.

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These uses: references in action.yml point to tags, not full commit SHAs: aws-actions/configure-aws-credentials@v4 (line 37), seemethere/upload-artifact-s3@v5 (lines 45, 54), actions/upload-artifact@v6 (lines 64, 72).

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

I fixed all six findings in hardened/action/action.yml, which is the only file in the action. Nothing was run or tested after the edits.

- **Script injection:** In the 'Check if binaries have changed' step, inputs.platform and inputs.version now go into the step's env: block as PLATFORM and VERSION. The two --s3-key arguments use "$PLATFORM/$VERSION/clang-tidy" and "$PLATFORM/$VERSION/clang-format" in double quotes, so the s3 keys come out the same as before.
- **Unpinned actions:** Each uses: reference now points to the full commit SHA its tag currently resolves to, with the tag kept as a trailing comment:
  - aws-actions/configure-aws-credentials v4 → 7474bc4690e29a8392af63c5b98e7449536d5c3a
  - seemethere/upload-artifact-s3 v5 → baba72d0712b404f646cebe0730933554ebce96a (both places it's used)
  - actions/upload-artifact v6 → b7c566a772e6b6bfb58ed0dc250532a479d7789f (both places it's used)

The inputs still appear in the with: values (s3-prefix and the artifact names). That's fine: with: values are passed to the action as data, not run by a shell, so they can't be used for injection.

