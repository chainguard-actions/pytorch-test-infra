<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20260922-155642** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Merge PR changes onto base' step puts ${{ inputs.head_sha }} and ${{ inputs.base_sha }} straight into the run: script, e.g. `git fetch origin "${{ inputs.head_sha }}"`, `git reset --hard "${{ inputs.base_sha }}"` and `git merge "${{ inputs.head_sha }}"`. The values are substituted into the script before bash runs, so the double quotes don't protect against injection. Fix: pass them through env vars (HEAD_SHA/BASE_SHA) and use "$HEAD_SHA"/"$BASE_SHA".

Locations:

- `action.yml:51`
- `action.yml:52`
- `action.yml:53`
- `action.yml:54`

### script-injection (severity: high)

Rule (a): the 'Build and run BC-linter' step puts expressions straight into the run: script, unquoted: `--base-commit=${{ inputs.base_sha }}`, `--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}`, `${{ inputs.suppression == 'true' && '--suppressed' || '' }}` and `${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}`. inputs.base_sha and inputs.config_dir are controlled by the caller. Fix: move them to env vars and expand them double-quoted, or with the guarded form ${VAR:+"$VAR"} for the optional flags.

Locations:

- `action.yml:71`
- `action.yml:72`
- `action.yml:73`
- `action.yml:74`

### script-injection (severity: high)

Rule (a): the 'Display documentation link if failed' step puts ${{ inputs.docs_link }} straight into the run: script: `echo "${{ inputs.docs_link }}"`. Fix: pass it through an env var and use echo "$DOCS_LINK".

Locations:

- `action.yml:80`

### unpinned-uses (severity: high)

The composite steps use tag refs instead of full commit SHAs: `uses: actions/checkout@v4` (line 30) and `uses: actions/checkout@v4` (line 36).

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

Moved inputs.head_sha, base_sha, docs_link, config_dir, suppression and steps.merge_changes.outputs.new_head_sha out of the run: scripts and into step env: blocks. The scripts now use them as double-quoted variables. The optional --suppressed and --config-dir flags are collected in a bash array that is empty when the flags aren't set, and the array is expanded safely under set -u. Pinned both actions/checkout@v4 uses to 11d5960a326750d5838078e36cf38b85af677262. No tests were run, so these changes have not been checked at runtime.

