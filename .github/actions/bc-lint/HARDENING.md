<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261123-205410** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite steps reference actions by mutable tag rather than a 40-char commit SHA: line 30 'uses: actions/checkout@v4' and line 36 'uses: actions/checkout@v4'.

Locations:

- `action.yml:30`
- `action.yml:36`

### script-injection (severity: high)

Rule (a): the 'Merge PR changes onto base' run block puts expressions straight into the shell script: 'git fetch origin "${{ inputs.head_sha }}"', 'git fetch origin "${{ inputs.base_sha }}"', 'git reset --hard "${{ inputs.base_sha }}"' and 'git merge "${{ inputs.head_sha }}"'. Pass the inputs through env: variables and expand them double-quoted.

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (a): the 'Build and run BC-linter' run block puts expressions straight into the shell script: '--base-commit=${{ inputs.base_sha }}', '--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}', '${{ inputs.suppression == 'true' && '--suppressed' || '' }}' and '${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}'. inputs.config_dir in particular can carry arbitrary shell metacharacters. Move them into env: variables and expand them double-quoted (or use the guarded ${VAR:+"..."} form for optional arguments).

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (a): the 'Display documentation link if failed' run block puts an expression straight into the shell script: 'echo "${{ inputs.docs_link }}"'. Route it through an env: variable and expand it as "$DOCS_LINK".

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

Pinned both actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262. Moved all inline ${{ }} expressions in run: blocks into env: (HEAD_SHA, BASE_SHA, NEW_HEAD_SHA, SUPPRESSION, CONFIG_DIR, DOCS_LINK). Optional --suppressed and --config-dir flags built via a bash array (set -u safe expansion) so they drop out when unset, preserving upstream argument behavior.

