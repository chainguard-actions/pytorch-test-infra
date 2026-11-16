<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--bc-lint/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--bc-lint/v20261029-163400** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Merge PR changes onto base' step puts ${{ inputs.head_sha }} and ${{ inputs.base_sha }} straight into the run script. Offending lines include: git fetch origin "${{ inputs.head_sha }}", git reset --hard "${{ inputs.base_sha }}" and git merge "${{ inputs.head_sha }}". The double quotes in the script don't help: the expression is filled in before the shell runs, so a value containing a quote character can run commands. Fix: map the inputs to env vars (e.g. HEAD_SHA, BASE_SHA) and use "$HEAD_SHA" / "$BASE_SHA" in the script.

Locations:

- `action.yml:51`
- `action.yml:52`
- `action.yml:53`
- `action.yml:54`

### script-injection (severity: high)

Rule (a): the 'Build and run BC-linter' step puts expressions straight into the run script, unquoted: --base-commit=${{ inputs.base_sha }}, --head-commit=${{ steps.merge_changes.outputs.new_head_sha }}, ${{ inputs.suppression == 'true' && '--suppressed' || '' }} and ${{ inputs.config_dir != '' && format('--config-dir={0}', inputs.config_dir) || '' }}. Whoever calls the action controls inputs.base_sha and inputs.config_dir, so either one can inject shell commands. Fix: pass these values through env vars and quote each expansion. For the optional config_dir, the guarded form ${CONFIG_DIR:+"--config-dir=$CONFIG_DIR"} keeps the argument out when it is empty.

Locations:

- `action.yml:71`
- `action.yml:72`
- `action.yml:73`
- `action.yml:74`

### script-injection (severity: high)

Rule (a): the 'Display documentation link if failed' step puts ${{ inputs.docs_link }} straight into the run script: echo "${{ inputs.docs_link }}". Fix: map it to an env var such as DOCS_LINK and use echo "$DOCS_LINK".

Locations:

- `action.yml:80`

### unpinned-uses (severity: high)

Two composite steps reference an action by tag instead of a full 40-character commit SHA: line 30 'uses: actions/checkout@v4' and line 36 'uses: actions/checkout@v4'. Pin both to a commit SHA.

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

I edited action.yml to fix all three finding types.

Script injection: every ${{ }} expression in the 'Merge PR changes onto base', 'Build and run BC-linter' and 'Display documentation link if failed' steps now goes through the step's env: block. The env vars are HEAD_SHA, BASE_SHA, NEW_HEAD_SHA, SUPPRESSION, CONFIG_DIR and DOCS_LINK, and each one is double-quoted wherever the script uses it.

Optional flags: '--suppressed' is now set inside the script, only when SUPPRESSION is 'true'. '--config-dir' uses the form ${CONFIG_DIR:+"--config-dir=$CONFIG_DIR"}. Both drop out completely when they're unset, the same as the original expressions did.

Pinning: both actions/checkout@v4 references now point to commit 11d5960a326750d5838078e36cf38b85af677262, with a '# v4' comment kept for readability.

I haven't run the action to test these changes.

