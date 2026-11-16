<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261109-192709** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts ${{ inputs.platform }} and ${{ inputs.version }} straight into its run: script, e.g. `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. Move them into env: variables (e.g. PLATFORM, VERSION) and use "$PLATFORM/$VERSION/..." with double quotes.

Locations:

- `action.yml:28`
- `action.yml:31`

### unpinned-uses (severity: high)

These composite action steps pin uses: to a mutable tag instead of a 40-character commit SHA: `uses: aws-actions/configure-aws-credentials@v4` (line 36), `uses: seemethere/upload-artifact-s3@v5` (lines 45, 54), `uses: actions/upload-artifact@v6` (lines 64, 72).

Locations:

- `action.yml:36`
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

In action.yml, the 'Check if binaries have changed' step no longer puts inputs.platform and inputs.version straight into its script. They now come in through the step's env: block as PLATFORM and VERSION, and the script uses them as "$PLATFORM/$VERSION/...". I also pinned every uses: to a full commit SHA, found with the SHA lookup tool, and kept the tag as a comment: aws-actions/configure-aws-credentials v4 -> 7474bc46..., seemethere/upload-artifact-s3 v5 -> baba72d0... (both steps), actions/upload-artifact v6 -> b7c566a7... (both steps). The expressions in with: inputs are not shell code, so I left them as they were. I haven't run the action or the analysis again to confirm the findings are gone.

