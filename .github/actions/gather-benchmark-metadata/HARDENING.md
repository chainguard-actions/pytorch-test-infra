<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261103-202628** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Gather the metadata' step puts the expression ${{ inputs.venv }} straight into the run: script, in `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script text before bash parses it, so a crafted venv input can run shell commands. Fix: add VENV: ${{ inputs.venv }} to the step's env: block and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

The composite step points to a branch, not a full commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a 40-character commit SHA.

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

Both script-injection findings and the unpinned action are fixed in hardened/action/action.yml. I haven't run the action to test these changes.

- **Script injection:** in the 'Gather the metadata' step, `${{ inputs.venv }}` was written straight into the shell script. It's now passed in through the step's `env:` block as `VENV`, and the script uses `"${VENV}"` in the `-n` check and the `source` line.
- **Unpinned action:** `pytorch/test-infra/.github/actions/get-workflow-job-id` was pinned to the `main` branch. It's now pinned to commit e9b5b0a4c36ebfde49dec880ae77705038009471 with a `# main` comment. That is the upstream commit this version was built from; I confirmed it exists with `lookup_action_sha`. Pinning to it, rather than today's tip of `main`, keeps the helper action on the same code as the rest of this release.

One possible problem I didn't change because it isn't a security finding: the step runs `${GITHUB_ACTION_PATH}/../../scripts/benchmarks/gather_metadata.py`, a script that lives elsewhere in the upstream repository. This folder contains only `action.yml`, so that script may not be there when the action is published from the mirror, and the step would then fail.

