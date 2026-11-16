<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261112-155209** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses mutable tag refs instead of full 40-character commit SHAs: 'uses: actions/checkout@v4' (line 30) and 'uses: actions/checkout@v4' (line 36).

Locations:

- `action.yml:30`
- `action.yml:36`

### script-injection (severity: high)

Rule (a): step 'Merge PR changes onto base' puts expressions straight into the run script: 'git fetch origin "${{ inputs.head_sha }}"', 'git fetch origin "${{ inputs.base_sha }}"', 'git reset --hard "${{ inputs.base_sha }}"', 'git merge "${{ inputs.head_sha }}"'. Quoting does not help because the values are substituted into the script text before the shell parses it.

Locations:

- `action.yml:51`
- `action.yml:52`
- `action.yml:53`
- `action.yml:54`

### script-injection (severity: high)

Rule (a): step 'Build and run BC-linter' puts unquoted expressions straight into the run script: '--base-commit=${{ inputs.base_sha }}', '--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}', '${{ inputs.suppression == 'true' && '--suppressed' || '' }}', '${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}'. inputs.config_dir is free text that the caller controls.

Locations:

- `action.yml:71`
- `action.yml:72`
- `action.yml:73`
- `action.yml:74`

### script-injection (severity: high)

Rule (a): step 'Display documentation link if failed' puts an expression straight into the run script: 'echo "${{ inputs.docs_link }}"'.

Locations:

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

Pinned both actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262. Moved every ${{ }} expression out of the run scripts and into env: blocks: head_sha/base_sha in the merge step; base_sha, new_head_sha, suppression and config_dir in the lint step; docs_link in the docs step. The optional --suppressed and --config-dir flags are now built in a bash array, and the expansion still works under set -u when neither flag is set, so the arguments come out the same as upstream's. --config-dir=<dir> stays one argument. Nothing was run to test the change.

