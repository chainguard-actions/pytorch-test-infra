<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261103-202628** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' (id: calculate-image) writes values taken from inputs to $GITHUB_OUTPUT without running them through printf '%s' ... | tr -d '\n\r' first. The inputs are DOCKER_IMAGE_NAME (inputs.docker-image-name), REPO_NAME (inputs.repo-name or github.event.repository.name), DOCKER_REGISTRY (inputs.docker-registry), CUSTOM_TAG_PREFIX (inputs.custom-tag-prefix) and the derived DOCKER_TAG. Affected lines: echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}", echo "docker-tag=${DOCKER_TAG}" >> "${GITHUB_OUTPUT}", echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" >> "${GITHUB_OUTPUT}" and echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" >> "${GITHUB_OUTPUT}". A value containing a newline can inject extra step outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:119`
- `action.yml:120`

### script-injection (severity: high)

Rule (b), 'Build docker image' step: this is the shell command passed to nick-fields/retry, run with shell: bash. Workflow-controlled data is expanded without quotes: `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)` expands DOCKER_IMAGE unquoted, and `${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..." -t "${DOCKER_IMAGE}"` expands inputs.docker-build-script unquoted and runs it as a command.

Locations:

- `action.yml:254`
- `action.yml:256`

### script-injection (severity: high)

Rule (b), steps 'Check if image should be built' and 'Login to ECR': the retry helper `retry () { $*  || (sleep 1 && $*) || (sleep 2 && $*) }` re-expands its arguments unquoted with $*. One of those arguments is DOCKER_REGISTRY (inputs.docker-registry), so a workflow-controlled value gets word-split and glob-expanded. Use "$@" instead.

Locations:

- `action.yml:141`
- `action.yml:213`

### unpinned-uses (severity: high)

action.yml uses a tag instead of a full 40-character commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:241`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

I fixed all four findings in action.yml. Nothing has been run or tested yet.

- **github-env-injection:** I added a `sanitize()` helper (`printf '%s' | tr -d '\n\r'`) to the calculate-image step. Every input-derived value written to $GITHUB_OUTPUT now goes through it: docker-image, docker-tag and custom-tag-prefix. sanitize only wraps plain variables, never a command substitution, so a failing command still stops the step under `set -e`.
- **script-injection, retry helper:** In both login steps the retry helper now uses `"$@"` instead of `$*`, so DOCKER_REGISTRY is passed as one argument and is no longer split on spaces or expanded as a glob.
- **script-injection, build step:** The value passed to awk is now in double quotes. `DOCKER_BUILD_SCRIPT` is split into an array with an unquoted assignment, the same way upstream's unquoted expansion split it, and then run as `"${BUILD_CMD[@]}"`. A script path with extra arguments still works as it did upstream, and nothing inside the value gets evaluated.
- **unpinned-uses:** `nick-fields/retry` is pinned to commit 7152eba30c6575329ac0576536151aca5a72780e, with a `# v3.0.0` comment.

