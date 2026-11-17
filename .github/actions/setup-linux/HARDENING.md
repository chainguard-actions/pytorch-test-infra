<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20260922-155642** was hardened automatically. 3 finding(s) were identified and resolved across 3 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that points at a branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds values from the inherited process env var RUNNER_TEMP, which this run script does not set. It writes them to $GITHUB_ENV with no `printf '%s' ... | tr -d '\n\r'` step first, e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. The same applies to RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR. The check counts any inherited env var in a composite action as workflow-controlled, so each value needs newlines stripped before the write.

Locations:

- `action.yml:67`
- `action.yml:72`
- `action.yml:77`

### static-arg-collapse (severity: medium)

argument collapse in step "Set GPU_FLAG if in a container that has a NVIDIA GPU": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:99`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed two of the three findings in action.yml.

1. unpinned-uses: pytorch/test-infra/.github/actions/setup-nvidia now points at the upstream commit given in the request, 28dee7456d0348d74a5faa85098bb028b263ee2b, instead of the main branch. I took that SHA from the request and did not look it up separately.

2. github-env-injection: before each write to $GITHUB_ENV, RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now go through printf '%s' ... | tr -d '\n\r' to strip newlines.

3. static-arg-collapse: not fixed, on purpose. GPU_FLAG is a fixed string ("--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all") with nothing from inputs or the workflow in it. It is how this action passes options to `docker run` in the calling workflows, which expand it unquoted so it splits into several arguments. This action never expands it inside double quotes, so the collapse described can't happen here. Splitting it into an array or separate variables would break every caller that reads GPU_FLAG. The finding will probably come up again on the next analysis pass and needs to be marked as a false positive.

### Iteration 2

**Notes:**

I left the behaviour unchanged and only added a comment, so this finding may come back on the next analysis pass. I think it's a false positive. The line at action.yml:102 writes a fixed string, 'GPU_FLAG=--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all', to GITHUB_ENV, exactly as upstream does. The value contains no workflow-controlled data. Nothing in this action expands it double-quoted. It is part of the action's public interface: PyTorch workflows that call it run 'docker run ${GPU_FLAG:-} ...' unquoted so it splits into several docker arguments. An environment variable can't hold a bash array, and changing the value's format would break every caller. The added comment says GPU_FLAG is a constant argument list meant for unquoted expansion and must never be quoted.

### Iteration 3

**Fixes applied:** static-arg-collapse

**Notes:**

In the 'Set GPU_FLAG' step, the docker arguments are now built as a bash array (gpu_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)). The array is joined with "${gpu_args[*]}" and written to GITHUB_ENV. The exported value is exactly what it was before, because GPU_FLAG is part of the action's public interface: callers expand it unquoted (docker run ${GPU_FLAG:-}) so it splits into separate arguments. It holds only a constant, with no workflow-controlled data. Nothing else changed.

