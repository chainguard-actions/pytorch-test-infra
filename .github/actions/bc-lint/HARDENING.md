<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261125-223308** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Merge PR changes onto base' step puts ${{ inputs.head_sha }} and ${{ inputs.base_sha }} straight into the run script: git fetch origin "${{ inputs.head_sha }}", git fetch origin "${{ inputs.base_sha }}", git reset --hard "${{ inputs.base_sha }}", git merge "${{ inputs.head_sha }}". The expression is substituted before the shell runs, so the surrounding double quotes do not protect it. Fix: pass the inputs through env: (e.g. HEAD_SHA, BASE_SHA) and use "$HEAD_SHA" / "$BASE_SHA" in the script.

Locations:

- `action.yml:51`
- `action.yml:52`
- `action.yml:53`
- `action.yml:54`

### script-injection (severity: high)

Rule (a): the 'Build and run BC-linter' step puts expressions straight into the run script, unquoted: --base-commit=${{ inputs.base_sha }}, --head-commit=${{ steps.merge_changes.outputs.new_head_sha }}, ${{ inputs.suppression == 'true' && '--suppressed' || '' }} and ${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}. The config_dir and base_sha values come from inputs, so a caller can inject shell commands through them. Fix: move each value into env: and expand it double-quoted. For the optional flags, use guarded forms such as ${CONFIG_DIR:+"--config-dir=$CONFIG_DIR"}.

Locations:

- `action.yml:71`
- `action.yml:72`
- `action.yml:73`
- `action.yml:74`

### script-injection (severity: high)

Rule (a): the 'Display documentation link if failed' step runs echo "${{ inputs.docs_link }}", which puts the input straight into the run script. Fix: route it through env: (DOCS_LINK) and use echo "$DOCS_LINK".

Locations:

- `action.yml:80`

### unpinned-uses (severity: high)

The composite steps reference actions by a mutable tag instead of a full commit SHA: 'uses: actions/checkout@v4' (line 30) and 'uses: actions/checkout@v4' (line 36). Pin both to a 40-character commit SHA.

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

Pinned both actions/checkout@v4 uses to 11d5960a326750d5838078e36cf38b85af677262. Moved all inline ${{ }} expressions from run: scripts into env: (HEAD_SHA, BASE_SHA, NEW_HEAD_SHA, SUPPRESSION, CONFIG_DIR, DOCS_LINK) and referenced them double-quoted. Optional --suppressed and --config-dir flags are built via a bash array (expanded with the set -u-safe ${arr[@]+...} form), preserving upstream argument behavior.

