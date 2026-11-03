<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261027-001733** was hardened automatically. 9 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Two composite steps pin actions to a version tag instead of a full 40-character commit SHA: line 30 `uses: actions/checkout@v4` and line 36 `uses: actions/checkout@v4`.

Locations:

- `action.yml:30`
- `action.yml:36`

### script-injection (severity: high)

Rule (a): `${{ ... }}` expressions are pasted directly into `run:` scripts in three steps. Step 'Merge PR changes onto base' (lines 51-54), e.g. `git fetch origin "${{ inputs.head_sha }}"`, `git reset --hard "${{ inputs.base_sha }}"`, `git merge "${{ inputs.head_sha }}"`. Step 'Build and run BC-linter' (lines 71-74): `--base-commit=${{ inputs.base_sha }}`, `--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}`, `${{ inputs.suppression == 'true' && '--suppressed' || '' }}`, `${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}`. Step 'Display documentation link if failed' (line 80): `echo "${{ inputs.docs_link }}"`. The inputs should be passed through `env:` variables and expanded with double quotes.

Locations:

- `action.yml:51`
- `action.yml:71`
- `action.yml:80`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.head_sha }}" appears directly in run: block of step "Merge PR changes onto base"; move to env: map

Locations:

- `action.yml:51`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.base_sha }}" appears directly in run: block of step "Merge PR changes onto base"; move to env: map

Locations:

- `action.yml:52`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.base_sha }}" appears directly in run: block of step "Merge PR changes onto base"; move to env: map

Locations:

- `action.yml:53`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.head_sha }}" appears directly in run: block of step "Merge PR changes onto base"; move to env: map

Locations:

- `action.yml:54`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.base_sha }}" appears directly in run: block of step "Build and run BC-linter"; move to env: map

Locations:

- `action.yml:71`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.suppression == 'true' && '--suppressed' || '' }}" appears directly in run: block of step "Build and run BC-linter"; move to env: map

Locations:

- `action.yml:73`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.docs_link }}" appears directly in run: block of step "Display documentation link if failed"; move to env: map

Locations:

- `action.yml:80`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection

**Notes:**

Pinned both actions/checkout@v4 uses to 11d5960a326750d5838078e36cf38b85af677262 (# v4). Moved all ${{ }} expressions in run: blocks (head_sha, base_sha, new_head_sha output, suppression, config_dir, docs_link) into step env: and referenced them as quoted shell variables. Optional --suppressed and --config-dir flags are now built in a bash array (expanded with the set -u-safe ${arr[@]+...} form) so they drop out when unset, preserving upstream behavior.

### Iteration 2

**Fixes applied:** script-injection, static-inline-injection

**Notes:**

In the 'Merge PR changes onto base' step, moved inputs.head_sha and inputs.base_sha into env vars (INPUT_HEAD_SHA, INPUT_BASE_SHA) and changed the git fetch, reset and merge commands to use "$INPUT_HEAD_SHA" and "$INPUT_BASE_SHA". Nothing else changed.

