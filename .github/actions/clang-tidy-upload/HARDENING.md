<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20260922-155642** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts expressions straight into the run: script: --s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy" and --s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format". The double quotes don't make this safe, because the value is pasted into the script before bash parses it. Fix: move the inputs into env: variables (e.g. PLATFORM, VERSION) and use "$PLATFORM/$VERSION/clang-tidy" in the script.

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These composite steps reference actions by tag instead of a 40-character commit SHA: aws-actions/configure-aws-credentials@v4, seemethere/upload-artifact-s3@v5 (used twice), actions/upload-artifact@v6 (used twice).

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

In action.yml, the 'Check if binaries have changed' step now takes inputs.platform and inputs.version through its env: block as PLATFORM and VERSION. The script reads them as "$PLATFORM/$VERSION/..." instead of having the expressions pasted into it. I pinned all five uses: lines to full commit SHAs found with lookup_action_sha, keeping the tag as a comment: aws-actions/configure-aws-credentials v4 (7474bc46...), seemethere/upload-artifact-s3 v5 (baba72d0..., both uses) and actions/upload-artifact v6 (b7c566a7..., both uses). I haven't run the action or a new analysis pass to confirm the findings are gone. The with: values that still use expressions (s3-prefix, artifact names) were left as they are, because they go to the actions as inputs and never pass through a shell.

