<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261027-001733** was hardened automatically. 4 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step points to a branch instead of a full commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a) was violated in the 'Gather the metadata' step: `${{ inputs.venv }}` is inserted directly into the run script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. Move it into an env var such as VENV and reference it as "$VENV".

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

Pinned pytorch/test-infra/.github/actions/get-workflow-job-id to the commit main points to now, 48c8ec0a3da135fd3b5024bf17b0d61b4ab1e81a, with a '# main' comment so the branch is still visible. In the 'Gather the metadata' step, inputs.venv now goes into a VENV variable in the step's env: block, and the script uses "${VENV}" in the -n check and the source line. Nothing else in the action changed. No tests were run.

### Iteration 2

**Fixes applied:** invalid-yaml

**Notes:**

Fixed the broken 'Gather the metadata' step in action.yml. A bad earlier edit had mashed the 'id:' line together with pieces of the env: block. I put back 'id: gather-metadata' so the benchmark-metadata output can find the step again, added 'shell: bash' (composite run steps require it), and restored a clean 'env:' block with SCHEMA_VERSION and VENV. The other env entries and the run script were left as they were. I re-read the file afterwards; I didn't run a YAML parser or the tests. Separate issue: the script calls ../../scripts/benchmarks/gather_metadata.py relative to the action folder, and that file isn't in this directory, so the step will only work if it's run from inside the full pytorch/test-infra repo.

