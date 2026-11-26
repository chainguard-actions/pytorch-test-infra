<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261103-202628** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step points to a branch, not a commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Whoever controls that branch can change the code this action runs. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), an expression placed directly in a run: block. The 'Gather the metadata' step puts `${{ inputs.venv }}` straight into the shell script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script text before the shell parses it, so a crafted input can inject commands. Move it into an env: variable (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

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

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection

**Notes:**

I made both fixes in action.yml.

1. Pinned `pytorch/test-infra/.github/actions/get-workflow-job-id`. It was on `@main`; it now points at the full commit SHA e9b5b0a4c36ebfde49dec880ae77705038009471, with a `# main` comment. That SHA is the request's upstream_commit, which is the same test-infra commit this action was built from, so the sub-action matches its own version. I didn't run lookup_action_sha: it would have given today's tip of main, not this commit.

2. In the 'Gather the metadata' step, moved `inputs.venv` out of the script and into `env:` as `VENV`. The script now uses `"${VENV}"` in place of the inline expression, in both the `-n` check and the `source` line. Behaviour is unchanged otherwise.

Nothing has been run or tested.

