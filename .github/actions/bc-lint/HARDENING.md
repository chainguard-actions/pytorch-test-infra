<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261029-163400** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): step 'Merge PR changes onto base' puts inputs directly into its run: script, e.g. `git fetch origin "${{ inputs.head_sha }}"`, `git reset --hard "${{ inputs.base_sha }}"` and `git merge "${{ inputs.head_sha }}"`. Move inputs.head_sha and inputs.base_sha into env: variables and use them double-quoted.

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (a): step 'Build and run BC-linter' puts expressions directly into its run: script: `--base-commit=${{ inputs.base_sha }}`, `--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}`, `${{ inputs.suppression == 'true' && '--suppressed' || '' }}` and `${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}`. inputs.config_dir is a free-form string, so it can inject commands. Move these into env: variables and use them double-quoted (the guarded form for optional arguments).

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (a): step 'Display documentation link if failed' puts an input directly into its run: script: `echo "${{ inputs.docs_link }}"`. Move it into an env: variable and use "$DOCS_LINK".

Locations:

- `action.yml:80`

### unpinned-uses (severity: high)

Two composite steps use a version tag instead of a commit SHA: `uses: actions/checkout@v4` on line 30 and `uses: actions/checkout@v4` on line 36.

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

**Fixes applied:** script-injection, unpinned-uses, static-inline-injection

**Notes:**

I fixed all the findings in action.yml. I haven't run the action to test these changes.

- **Pinned checkout:** both `actions/checkout@v4` steps now point to commit 11d5960a326750d5838078e36cf38b85af677262, with `# v4` kept as a comment.
- **Merge PR changes onto base:** `inputs.head_sha` and `inputs.base_sha` are now passed in through `env:` as `HEAD_SHA` and `BASE_SHA`, and the script uses them double-quoted.
- **Build and run BC-linter:** the base SHA, the new head SHA, `suppression` and `config_dir` are now passed in through `env:`. The optional `--suppressed` and `--config-dir=` flags are collected in a bash array, so each one reaches the command as a separate argument. If neither applies, nothing extra is passed, the same as before. The array is expanded with the `${arr[@]+...}` form so `set -u` doesn't stop the script when it's empty.
- **Display documentation link:** `docs_link` is now passed through `env:` and printed with `echo "$DOCS_LINK"`.

