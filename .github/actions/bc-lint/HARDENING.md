<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261027-001733** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Two composite steps pin an action to a movable tag instead of a full commit SHA: line 30 'uses: actions/checkout@v4' and line 36 'uses: actions/checkout@v4'. Pin both to a 40-character commit SHA.

Locations:

- `action.yml:30`
- `action.yml:36`

### script-injection (severity: high)

Rule (a): in the 'Merge PR changes onto base' step, input expressions are pasted straight into the run: script. Lines 51-54: 'git fetch origin "${{ inputs.head_sha }}"', 'git fetch origin "${{ inputs.base_sha }}"', 'git reset --hard "${{ inputs.base_sha }}"' and 'git merge "${{ inputs.head_sha }}"'. Move these values into env: variables and expand them double-quoted.

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (a): in the 'Build and run BC-linter' step, expressions are pasted straight into the run: script without quotes. Line 71: '--base-commit=${{ inputs.base_sha }}'. Line 72: '--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}'. Line 73: '${{ inputs.suppression == 'true' && '--suppressed' || '' }}'. Line 74: '${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}'. Move these values into env: variables and expand them double-quoted. For the optional arguments, use the guarded form ${VAR:+"$VAR"}.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (a): in the 'Display documentation link if failed' step, line 80 pastes an input straight into the run: script: 'echo "${{ inputs.docs_link }}"'. Move it into an env: variable and expand it double-quoted.

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

Pinned both actions/checkout@v4 uses to 11d5960a326750d5838078e36cf38b85af677262 (# v4). Moved all ${{ }} expressions in run: blocks (head_sha, base_sha, new_head_sha output, suppression/config_dir flags, docs_link) into step env: and referenced them as double-quoted shell variables; optional flags use ${VAR:+"$VAR"} so empty values drop out as upstream's empty expressions did. The --config-dir=<value> flag stays a single '='-joined argument, the same as upstream.

