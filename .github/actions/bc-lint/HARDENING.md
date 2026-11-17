<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261112-155209** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references actions by a mutable tag, not a full commit SHA: line 30 'uses: actions/checkout@v4' and line 36 'uses: actions/checkout@v4'. Pin both to a 40-character commit SHA.

Locations:

- `action.yml:30`
- `action.yml:36`

### script-injection (severity: high)

Rule (a): the 'Merge PR changes onto base' step puts expressions straight into the run: script, e.g. 'git fetch origin "${{ inputs.head_sha }}"', 'git reset --hard "${{ inputs.base_sha }}"' and 'git merge "${{ inputs.head_sha }}"'. Pass inputs.head_sha and inputs.base_sha through env: and use them as "$HEAD_SHA" and "$BASE_SHA".

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (a): the 'Build and run BC-linter' step puts expressions straight into the run: script, unquoted: '--base-commit=${{ inputs.base_sha }}', '--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}', '${{ inputs.suppression == 'true' && '--suppressed' || '' }}' and '${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}'. inputs.config_dir is free text, so whatever the caller passes runs as shell code. Move these values into env: and quote them, using the guarded ${VAR:+"$VAR"} form for the optional flags.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (a): the 'Display documentation link if failed' step puts an input straight into the run: script: 'echo "${{ inputs.docs_link }}"'. Pass it through env: and use echo "$DOCS_LINK".

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

Pinned both actions/checkout@v4 references to 11d5960a326750d5838078e36cf38b85af677262. Moved inputs.head_sha, inputs.base_sha, steps.merge_changes.outputs.new_head_sha, inputs.suppression, inputs.config_dir and inputs.docs_link into step env: blocks. They are now used as quoted shell variables. The optional --suppressed and --config-dir flags are built in the shell and passed with the ${VAR:+"$VAR"} form, so they drop out when empty, as they did upstream. --config-dir=<value> stays one joined argument. I haven't run the action after these changes.

