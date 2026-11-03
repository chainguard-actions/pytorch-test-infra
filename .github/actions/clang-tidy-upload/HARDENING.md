<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261027-001733** was hardened automatically. 6 finding(s) were identified and resolved across 3 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) direct expression interpolation. In the 'Check if binaries have changed' run: block, inputs expressions are placed straight into the shell command: `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. To fix this, pass inputs.platform and inputs.version in through env: and reference them as "$PLATFORM" and "$VERSION", with double quotes.

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

These uses: references point to a mutable tag instead of a 40-character commit SHA: `aws-actions/configure-aws-credentials@v4` (line 37), `seemethere/upload-artifact-s3@v5` (line 44), `seemethere/upload-artifact-s3@v5` (line 53), `actions/upload-artifact@v6` (line 63) and `actions/upload-artifact@v6` (line 71).

Locations:

- `action.yml:37`
- `action.yml:44`
- `action.yml:53`
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

Moved inputs.platform and inputs.version out of the 'Check if binaries have changed' run: block. They are now set in the step's env: as PLATFORM and VERSION and used in the script as "$PLATFORM/$VERSION/...". Pinned 5 uses: references to full commit SHAs, each with a trailing comment naming its tag: aws-actions/configure-aws-credentials@v4 (7474bc46...), seemethere/upload-artifact-s3@v5 (baba72d0..., 2 places) and actions/upload-artifact@v6 (b7c566a7..., 2 places). I haven't run the action or re-run the analysis to confirm these changes.

### Iteration 2

**Fixes applied:** script-injection, unpinned-uses, invalid-yaml

**Notes:**

I fixed all three findings in action.yml. I didn't run or re-parse the file afterwards, so the next analysis pass will be the first real check.

- **script-injection:** The 'Check if binaries have changed' step no longer puts `inputs.platform` and `inputs.version` straight into its script. They are now passed in through an `env:` block as `PLATFORM` and `VERSION`, and the script uses "$PLATFORM/$VERSION/...".
- **unpinned-uses:** I pinned `aws-actions/configure-aws-credentials` to 7474bc4690e29a8392af63c5b98e7449536d5c3a (v4). Both `seemethere/upload-artifact-s3` steps are pinned to baba72d0712b404f646cebe0730933554ebce96a (v5). I looked up both SHAs rather than guessing them.
- **invalid-yaml:** A failed earlier edit had merged the pinned ref, the step name and the `if:` condition into one broken line in each S3 upload step. I split them back into separate `name:`, `uses:` and `if:` keys, so each upload is again skipped unless `upload-to-s3` is true. The broken lines no longer had the original step names, so I named the steps "Upload clang-tidy to s3" and "Upload clang-format to s3"; these may differ from upstream's names.

### Iteration 3

**Fixes applied:** script-injection, unpinned-uses, invalid-yaml

**Notes:**

Moved inputs.platform/version into env vars (INPUT_PLATFORM/INPUT_VERSION) in the check step; pinned aws-actions/configure-aws-credentials@v4 to 7474bc4690e29a8392af63c5b98e7449536d5c3a; repaired the malformed s3 upload step (restored name 'Upload clang-tidy to s3', SHA-pinned uses, and separate if: condition), which fixes the YAML parse error.

