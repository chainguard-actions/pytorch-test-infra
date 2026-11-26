<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action's steps pull in other actions by the mutable branch ref @main, not by a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 120). Anyone who can push to that branch can change the code these steps run. Pin each one to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:120`

### github-env-injection (severity: high)

The 'Install dependencies' step runs 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is an environment variable this composite action inherits; the run script doesn't set it. The value goes into $GITHUB_ENV without first passing through printf '%s' ... | tr -d '\n\r'. Strip newlines and carriage returns before the write and quote "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I pinned the two nested pytorch/test-infra actions (setup-uv and get-workflow-job-id) to e9b5b0a4c36ebfde49dec880ae77705038009471. That is the upstream commit this version was built from, as given in the request; I didn't look it up separately. They now read @<sha> # v20261103-202628 instead of @main.

The VIRTUAL_ENV write in 'Install dependencies' now strips newlines and carriage returns with printf '%s' | tr -d '\n\r' before it goes into $GITHUB_ENV, and "$GITHUB_ENV" is now quoted.

I also made two changes that weren't in the findings. The DEVICE_TYPE value written to $GITHUB_ENV is now sanitized the same way, because it comes from command output. The DEVICE_NAME write now quotes "$GITHUB_ENV".

Nothing has been run to test these changes.

