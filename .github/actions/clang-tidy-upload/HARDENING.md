<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261112-155209** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts ${{ inputs.platform }} and ${{ inputs.version }} straight into the run: script, e.g. `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. Fix: pass these inputs to the step through env: and refer to them as double-quoted shell variables.

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These uses: references point to version tags, not full commit SHAs: `aws-actions/configure-aws-credentials@v4` (line 37), `seemethere/upload-artifact-s3@v5` (lines 45, 54), `actions/upload-artifact@v6` (lines 64, 72).

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

Both findings are fixed in action.yml. I haven't run the action to test it.

- **Script injection:** The 'Check if binaries have changed' step no longer pastes `inputs.platform` and `inputs.version` into the script. They now go in through the step's `env:` block as `INPUT_PLATFORM` and `INPUT_VERSION`, and the script uses them as double-quoted shell variables. The script runs the same commands as before.
- **Unpinned actions:** I looked up each version tag and pinned all five `uses:` lines to its full commit SHA, keeping the tag as a comment:
  - `aws-actions/configure-aws-credentials` v4 → 7474bc4690e29a8392af63c5b98e7449536d5c3a
  - `seemethere/upload-artifact-s3` v5 (both uses) → baba72d0712b404f646cebe0730933554ebce96a
  - `actions/upload-artifact` v6 (both uses) → b7c566a772e6b6bfb58ed0dc250532a479d7789f

The `${{ }}` expressions in the `with:` inputs (`s3-prefix` and the artifact names) are still there. They aren't run by a shell, so they can't inject commands.

