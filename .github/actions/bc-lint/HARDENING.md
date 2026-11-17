<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20260922-155642** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps reference actions by mutable tag instead of a full 40-char commit SHA: line 30 'uses: actions/checkout@v4' and line 36 'uses: actions/checkout@v4'.

Locations:

- `action.yml:30`
- `action.yml:36`

### script-injection (severity: high)

Rule (a): the 'Merge PR changes onto base' step puts expressions straight into the run script: 'git fetch origin "${{ inputs.head_sha }}"', 'git fetch origin "${{ inputs.base_sha }}"', 'git reset --hard "${{ inputs.base_sha }}"' and 'git merge "${{ inputs.head_sha }}"'. A value containing quotes or $(...) can run shell commands. Pass the inputs through env: and use "$HEAD_SHA" / "$BASE_SHA" in the script.

Locations:

- `action.yml:51`
- `action.yml:52`
- `action.yml:53`
- `action.yml:54`

### script-injection (severity: high)

Rule (a): the 'Build and run BC-linter' step puts expressions straight into the run script, unquoted: '--base-commit=${{ inputs.base_sha }}', '--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}', '${{ inputs.suppression == 'true' && '--suppressed' || '' }}' and '${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}'. A crafted inputs.base_sha or inputs.config_dir can run any command. Pass these through env: and use double-quoted expansions, with the ${VAR:+"..."} form for the optional flags.

Locations:

- `action.yml:71`
- `action.yml:72`
- `action.yml:73`
- `action.yml:74`

### script-injection (severity: high)

Rule (a): the 'Display documentation link if failed' step puts an expression straight into the run script: 'echo "${{ inputs.docs_link }}"'. A docs_link containing quotes or $(...) can run commands. Pass it through env: (DOCS_LINK) and use echo "$DOCS_LINK".

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

Pinned both actions/checkout@v4 references to 11d5960a326750d5838078e36cf38b85af677262 (# v4). Moved inputs.head_sha/base_sha, the merge step output, suppression, config_dir and docs_link into step env: blocks and referenced them as quoted shell variables. Optional --suppressed / --config-dir flags are built in a bash array (each flag stays its own argument; the array expansion is guarded so it works with set -u on older bash).

