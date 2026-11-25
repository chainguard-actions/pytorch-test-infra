<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261125-022556** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' writes values derived from untrusted inputs (inputs.docker-image-name, inputs.docker-registry, inputs.repo-name/github.event.repository.name, inputs.custom-tag-prefix) to $GITHUB_OUTPUT without the printf '%s' ... | tr -d '\n\r' sanitization step. Examples: echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"; echo "docker-tag=${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"; echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"; echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" >> "${GITHUB_OUTPUT}". A newline in an input can inject arbitrary additional step outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### unpinned-uses (severity: high)

Composite step 'Build docker image' references an action by mutable tag rather than a 40-char commit SHA: 'uses: nick-fields/retry@v3.0.0'.

Locations:

- `action.yml:234`

### script-injection (severity: high)

Rule (b): The shell script executed in the 'Build docker image' step (nick-fields/retry 'command:') expands workflow-controlled data without quoting: 'IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)' expands DOCKER_IMAGE (step output from inputs.docker-image-name) unquoted, and '${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..." -t "${DOCKER_IMAGE}"' expands inputs.docker-build-script unquoted, so word splitting and glob expansion apply to it. Also, the retry() helpers in 'Check if image should be built' and 'Login to ECR' re-expand their arguments (including DOCKER_REGISTRY from inputs.docker-registry) as unquoted '$*'.

Locations:

- `action.yml:246`
- `action.yml:248`
- `action.yml:141`
- `action.yml:212`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, unpinned-uses, script-injection

**Notes:**

I fixed all three findings in action.yml.

1. Output injection: the 'Calculate docker image' step now has a sanitize() helper that runs printf '%s' | tr -d '\n\r'. Each value is stored in a variable first, then written to $GITHUB_OUTPUT: docker-image, docker-tag and custom-tag-prefix in all three branches. Nothing is wrapped inside another command's arguments, so a failing command still stops the step.

2. Unpinned action: nick-fields/retry is now pinned to commit 7152eba30c6575329ac0576536151aca5a72780e (v3.0.0), resolved with lookup_action_sha.

3. Script injection:
- Both retry() helpers ('Check if image should be built' and 'Login to ECR') used an unquoted $*. They now use "$@", so the registry argument is passed through intact.
- In 'Build docker image', DOCKER_IMAGE is now quoted when IMAGE_NAME is computed (printf '%s\n' instead of an unquoted echo).
- "${DOCKER_BUILD_SCRIPT}" is now quoted. It is a single script path, and the first step already checks it as one file with -f, so quoting doesn't change how it's used.

Nothing has been run or tested. One behaviour change: if a caller passes extra arguments in docker-build-script (something like './build.sh --foo'), they are now read as part of the file name. The upstream unquoted form split them off as separate arguments. That kind of value would already fail the step-one file check, so I don't expect it in practice.

