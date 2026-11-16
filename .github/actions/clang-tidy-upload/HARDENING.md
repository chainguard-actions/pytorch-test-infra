<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261109-232755** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts expressions straight into the run: script: `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. A crafted input value can break out of the quotes and run its own shell commands. Fix: pass the inputs in through env: variables and use them double-quoted in the script.

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

action.yml points to actions by mutable tags instead of 40-character commit SHAs: aws-actions/configure-aws-credentials@v4 (line 37), seemethere/upload-artifact-s3@v5 (lines 45, 54), and actions/upload-artifact@v6 (lines 64, 72).

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

I fixed all three findings in action.yml.

- **Script injection (`script-injection` and `static-inline-injection`):** the 'Check if binaries have changed' step no longer pastes `inputs.platform` and `inputs.version` into its script. They now come in through the step's env: block as `INPUT_PLATFORM` and `INPUT_VERSION`, and the script uses them double-quoted.
- **Unpinned actions (`unpinned-uses`):** every action reference now uses a full commit SHA, with the original tag kept as a comment. I looked up each SHA with the lookup tool:
  - `aws-actions/configure-aws-credentials` v4: `7474bc4690e29a8392af63c5b98e7449536d5c3a`
  - `seemethere/upload-artifact-s3` v5: `baba72d0712b404f646cebe0730933554ebce96a` (2 uses)
  - `actions/upload-artifact` v6: `b7c566a772e6b6bfb58ed0dc250532a479d7789f` (2 uses)

I haven't run the action or a new analysis pass, so these changes are untested.

