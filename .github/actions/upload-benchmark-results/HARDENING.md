<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-192709** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps reference actions by a mutable branch instead of a full 40-char commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes a value built from the inherited process env var RUNNER_TEMP straight to $GITHUB_ENV with no sanitization step before it: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is not set by this run: script. The check says any write whose source is not a literal computed in the same block needs printf '%s' ... | tr -d '\n\r' first. This is a borderline case: the runner normally sets RUNNER_TEMP, so an attacker would only control it if the calling workflow overrides it.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml.

- **unpinned-uses:** The two `pytorch/test-infra` sub-actions (`setup-uv` and `get-workflow-job-id`) pointed at the `main` branch. They now point at commit 0569df511711f70601c984fe3a93dac324afc9ce, which is the upstream commit this mirror version was built from, with a `# main` comment kept for readability. I checked that the SHA resolves with `lookup_action_sha`. Using this commit rather than whatever `main` points to today keeps the sub-actions at the same version as the rest of this action.
- **github-env-injection:** The `VIRTUAL_ENV` value is built from `RUNNER_TEMP`. It now goes through `printf '%s' ... | tr -d '\n\r'` before being written to `$GITHUB_ENV`, and `$GITHUB_ENV` is now quoted. The capture is a plain assignment and composite `bash` steps run with `pipefail`, so a failure there still stops the step.

I haven't run the action after these changes.

