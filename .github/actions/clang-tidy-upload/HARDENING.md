<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--clang-tidy-upload/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--clang-tidy-upload/v20261029-163400** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Check if binaries have changed' step puts GitHub Actions expressions straight into its run: script: `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-tidy"` and `--s3-key "${{ inputs.platform }}/${{ inputs.version }}/clang-format"`. To fix it, move inputs.platform and inputs.version into env: variables and reference them double-quoted (e.g. "$PLATFORM/$VERSION/clang-tidy").

Locations:

- `action.yml:29`
- `action.yml:32`

### unpinned-uses (severity: high)

Five composite steps reference actions by a mutable tag instead of a full 40-character commit SHA: `uses: aws-actions/configure-aws-credentials@v4` (line 37), `uses: seemethere/upload-artifact-s3@v5` (lines 44 and 53) and `uses: actions/upload-artifact@v6` (lines 63 and 71).

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

I fixed all six findings in action.yml.

- **Script injection (the 'Check if binaries have changed' step):** `inputs.platform` and `inputs.version` now go into the step's `env:` block as `PLATFORM` and `VERSION`. The script uses them in double quotes, as `"$PLATFORM/$VERSION/clang-tidy"` and `"$PLATFORM/$VERSION/clang-format"`. Both inputs are required single values, so the arguments passed to `check_s3.py` are unchanged.
- **Unpinned actions:** all five `uses:` lines now point at a full commit SHA, with the original tag kept as a comment:
  - `aws-actions/configure-aws-credentials` → `7474bc4690e29a8392af63c5b98e7449536d5c3a` (v4)
  - `seemethere/upload-artifact-s3`, both steps → `baba72d0712b404f646cebe0730933554ebce96a` (v5)
  - `actions/upload-artifact`, both steps → `b7c566a772e6b6bfb58ed0dc250532a479d7789f` (v6)

I haven't run the action or any tests. The `${{ }}` expressions left in the `with:` and `if:` fields were not flagged because they don't go through a shell.

