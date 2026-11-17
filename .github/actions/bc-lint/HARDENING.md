<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261021-234439** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a), step 'Merge PR changes onto base': inputs.head_sha and inputs.base_sha are pasted directly into the run script, e.g. `git fetch origin "${{ inputs.head_sha }}"`, `git reset --hard "${{ inputs.base_sha }}"` and `git merge "${{ inputs.head_sha }}"`.

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (a), step 'Build and run BC-linter': inputs and step outputs are pasted directly into the run script, unquoted: `--base-commit=${{ inputs.base_sha }}`, `--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}`, `${{ inputs.suppression == 'true' && '--suppressed' || '' }}` and `${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}`.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (a), step 'Display documentation link if failed': `echo "${{ inputs.docs_link }}"` pastes inputs.docs_link directly into the run script.

Locations:

- `action.yml:80`

### unpinned-uses (severity: high)

The composite steps point to a version tag instead of a full commit SHA: `uses: actions/checkout@v4` on line 30 and `uses: actions/checkout@v4` on line 36.

Locations:

- `action.yml:30`
- `action.yml:36`

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

**Fixes applied:** script-injection, static-inline-injection, unpinned-uses

**Notes:**

Pinned both actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262. Moved inputs.head_sha, base_sha, docs_link, suppression, config_dir and step output new_head_sha into env: blocks; rebuilt optional --suppressed / --config-dir flags with a bash array (empty-safe under set -u) so argument boundaries match upstream.

