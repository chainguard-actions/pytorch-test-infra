<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261109-192709** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Merge PR changes onto base' step puts ${{ inputs.head_sha }} and ${{ inputs.base_sha }} directly into the run: script, e.g. `git fetch origin "${{ inputs.head_sha }}"`, `git reset --hard "${{ inputs.base_sha }}"` and `git merge "${{ inputs.head_sha }}"`. The double quotes don't help, because the value is substituted into the script text before the shell runs. Fix: pass the inputs through env: variables (e.g. HEAD_SHA, BASE_SHA) and use "$HEAD_SHA" and "$BASE_SHA" in the script.

Locations:

- `action.yml:51`
- `action.yml:52`
- `action.yml:53`
- `action.yml:54`

### script-injection (severity: high)

Rule (a): the 'Build and run BC-linter' step puts expressions directly into the run: script without quotes: `--base-commit=${{ inputs.base_sha }}`, `--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}`, `${{ inputs.suppression == 'true' && '--suppressed' || '' }}` and `${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}`. config_dir and base_sha are free-text values supplied by the caller. Fix: pass them through env: variables and quote each one, using the ${VAR:+"$VAR"} form for the optional arguments.

Locations:

- `action.yml:71`
- `action.yml:72`
- `action.yml:73`
- `action.yml:74`

### script-injection (severity: high)

Rule (a): the 'Display documentation link if failed' step puts an input directly into the script: `echo "${{ inputs.docs_link }}"`. Fix: pass it through an env: variable and use echo "$DOCS_LINK".

Locations:

- `action.yml:80`

### unpinned-uses (severity: high)

Two composite steps use a version tag instead of a full commit SHA: `uses: actions/checkout@v4` (line 30, the pytorch/test-infra checkout) and `uses: actions/checkout@v4` (line 36, the repo checkout). Pin both to a 40-character commit SHA.

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

Pinned both actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262. Moved head_sha, base_sha, new_head_sha, suppression flag, config_dir and docs_link into step env: blocks and referenced them as quoted shell vars; optional args use ${VAR:+...} so they drop out when empty, preserving upstream argument behavior.

