<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261125-022556** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point to a mutable tag instead of a full 40-character commit SHA: 'uses: actions/checkout@v4' (line 30, checkout of pytorch/test-infra) and 'uses: actions/checkout@v4' (line 36, checkout of the PR repo).

Locations:

- `action.yml:30`
- `action.yml:36`

### script-injection (severity: high)

Rule (a): the 'Merge PR changes onto base' step puts expressions straight into the run: script, e.g. 'git fetch origin "${{ inputs.head_sha }}"', 'git fetch origin "${{ inputs.base_sha }}"', 'git reset --hard "${{ inputs.base_sha }}"' and 'git merge "${{ inputs.head_sha }}" || MERGE_CONFLICT=1'. Move them into env: variables and expand them double-quoted.

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (a): the 'Build and run BC-linter' step puts expressions straight into the run: script and leaves them unquoted: '--base-commit=${{ inputs.base_sha }}', '--head-commit=${{ steps.merge_changes.outputs.new_head_sha }}', '${{ inputs.suppression == 'true' && '--suppressed' || '' }}' and '${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}'. A crafted config_dir or base_sha could inject shell commands.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (a): the 'Display documentation link if failed' step puts an input straight into the run: script: 'echo "${{ inputs.docs_link }}"'.

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

Pinned both actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262. Moved head_sha, base_sha, new_head_sha, suppression, config_dir and docs_link into step env: and referenced them as double-quoted shell variables. The optional --suppressed and --config-dir flags are built with a bash array, using the ${arr[@]+...} form so set -u does not fail on an empty array. This means an empty flag drops out instead of passing an empty argument.

