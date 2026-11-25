<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261109-232755** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Gather the metadata' step puts the expression ${{ inputs.venv }} straight into the run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The template is filled in before bash parses the script, so a value containing a double quote or $(...) can run arbitrary commands. Fix: map inputs.venv to an env var (e.g. VENV) and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

A composite step points to a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:38`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.venv }}" appears directly in run: block of step "Gather the metadata"; move to env: map

Locations:

- `action.yml:57`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.venv }}" appears directly in run: block of step "Gather the metadata"; move to env: map

Locations:

- `action.yml:58`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, static-inline-injection, unpinned-uses

**Notes:**

I fixed all four findings in action.yml.

- **Script injection (`script-injection` and both `static-inline-injection` findings):** the 'Gather the metadata' step put `${{ inputs.venv }}` straight into its script. That value now goes in the step's env: block as `VENV`, and the script uses `"${VENV}"` in both the `-n` check and the `source` line.
- **Unpinned action (`unpinned-uses`):** `pytorch/test-infra/.github/actions/get-workflow-job-id@main` now points to commit 2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f, with a `# main` comment. That is the upstream commit this mirror version was built from, so the sub-action matches the rest of the action rather than whatever is on `main` today. Looking up that SHA confirmed it exists in pytorch/test-infra.

Nothing has been run or tested yet.

