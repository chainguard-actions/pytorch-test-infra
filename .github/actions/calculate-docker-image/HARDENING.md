<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261109-232755** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' writes values taken from workflow inputs to $GITHUB_OUTPUT without first stripping newlines with printf '%s' ... | tr -d '\n\r'. The values are DOCKER_IMAGE_NAME (inputs.docker-image-name), REPO_NAME (inputs.repo-name or github.event.repository.name), DOCKER_REGISTRY (inputs.docker-registry), CUSTOM_TAG_PREFIX (inputs.custom-tag-prefix or part of the image name) and DOCKER_TAG, which is built from those. Examples: echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}", echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" >> "${GITHUB_OUTPUT}" and echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" >> "${GITHUB_OUTPUT}". A value containing a newline can inject extra step outputs, and later steps use those outputs in shell commands.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:114`
- `action.yml:115`
- `action.yml:116`

### script-injection (severity: high)

Rule (b): step 'Build docker image' runs a shell script through the command field of nick-fields/retry. That script expands workflow-controlled env vars without double quotes. One line is: IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk -F '[:,]' '{print $1}'). DOCKER_IMAGE comes from a step output built from inputs, and here it is split on whitespace and glob-expanded. The other line is: ${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..." -t "${DOCKER_IMAGE}". DOCKER_BUILD_SCRIPT (inputs.docker-build-script) is expanded unquoted and run as a command, so it is split on whitespace.

Locations:

- `action.yml:258`
- `action.yml:260`

### unpinned-uses (severity: high)

The composite action step 'Build docker image' pins a version tag instead of a full 40-character commit SHA: uses: nick-fields/retry@v3.0.0

Locations:

- `action.yml:245`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

I fixed all three findings in action.yml. I haven't run or tested the changed action.

- **github-env-injection:** The 'Calculate docker image' step has a new `sanitize()` helper that runs `printf '%s' "$1" | tr -d '\n\r'`. Every value the step writes to $GITHUB_OUTPUT (docker-image, docker-tag, custom-tag-prefix) is now saved to a variable as `X="$(sanitize ...)"` first, then written.
- **script-injection:** In the 'Build docker image' retry command, the image path is now passed to awk double-quoted via `printf '%s\n'` instead of an unquoted `echo`. `DOCKER_BUILD_SCRIPT` is turned into an array with an unquoted assignment, `build_cmd=(${DOCKER_BUILD_SCRIPT})`, and run as `"${build_cmd[@]}"`. That splits and globs exactly like upstream's unquoted call, so a script path with arguments still works.
- **unpinned-uses:** `nick-fields/retry@v3.0.0` is now pinned to `7152eba30c6575329ac0576536151aca5a72780e # v3.0.0`.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

Replaced unquoted $* with "$@" in the retry() helper in both the 'Check if image should be built' and 'Login to ECR' steps of action.yml, so DOCKER_REGISTRY is no longer re-split or glob-expanded.

