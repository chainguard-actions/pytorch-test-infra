<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261119-192116** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references actions by mutable tag rather than a 40-char commit SHA: 'uses: actions/checkout@v4' (line 30) and 'uses: actions/checkout@v4' (line 36).

Locations:

- `action.yml:30`
- `action.yml:36`

### script-injection (severity: high)

Rule (a): step 'Merge PR changes onto base' interpolates expressions directly into the run script: 'git fetch origin "${{ inputs.head_sha }}"', 'git fetch origin "${{ inputs.base_sha }}"', 'git reset --hard "${{ inputs.base_sha }}"', 'git merge "${{ inputs.head_sha }}"'. Move these into env: variables and reference them as "$VAR".

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (a): step 'Build and run BC-linter' interpolates expressions directly and unquoted into the run script: '--base-commit=${{ inputs.base_sha }}', '--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}', '${{ inputs.suppression == 'true' && '--suppressed' || '' }}', '${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}'. inputs.config_dir is free-form text, so it can inject shell commands.

Locations:

- `action.yml:72`

### script-injection (severity: high)

Rule (a): step 'Display documentation link if failed' interpolates an input directly into the run script: 'echo "${{ inputs.docs_link }}"'.

Locations:

- `action.yml:81`

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

Pinned both actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262. Moved inputs.head_sha, inputs.base_sha, the merge step output, suppression, config_dir and docs_link into step env: vars, quoted every use. The optional flags --suppressed and --config-dir are now built in a bash array, so an empty value adds no argument and the argument boundaries match upstream. The test-infra checkout ref was left as upstream had it.

