<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20260922-155642** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' writes values taken from workflow-controlled inputs to $GITHUB_OUTPUT without first running them through printf '%s' ... | tr -d '\n\r'. The values are DOCKER_IMAGE_NAME (inputs.docker-image-name), DOCKER_REGISTRY (inputs.docker-registry), REPO_NAME (inputs.repo-name or github.event.repository.name), CUSTOM_TAG_PREFIX (inputs.custom-tag-prefix or derived from the image name) and DOCKER_TAG (derived from them). Examples: echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"; echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"; echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" >> "${GITHUB_OUTPUT}". A value containing a newline could inject extra step outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### script-injection (severity: high)

Rule (b): in step 'Check if image should be built', the retry helper expands its arguments unquoted as `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. It is called as `retry login "${DOCKER_REGISTRY}"`, so the workflow-controlled inputs.docker-registry value is split and glob-expanded again without quotes. Use "$@" instead.

Locations:

- `action.yml:142`

### script-injection (severity: high)

Rule (b): in step 'Login to ECR', the retry helper expands its arguments unquoted as `$*  || (sleep 1 && $*) || (sleep 2 && $*)`. It is called as `retry login "${DOCKER_REGISTRY}"`, so the workflow-controlled inputs.docker-registry value is split and glob-expanded again without quotes. Use "$@" instead.

Locations:

- `action.yml:213`

### script-injection (severity: high)

Rule (b): in step 'Build docker image', the shell script passed to nick-fields/retry as `command:` (bash runs it) expands workflow-controlled data without quotes. `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | ...)` uses DOCKER_IMAGE, which comes from step outputs built from inputs. `${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..."` takes inputs.docker-build-script unquoted and runs it as a command.

Locations:

- `action.yml:247`
- `action.yml:249`

### unpinned-uses (severity: high)

The composite step 'Build docker image' references an action by version tag instead of a full commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:235`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

All findings are fixed in action.yml.
- Step outputs: I added a sanitize() helper (printf '%s' | tr -d '\n\r') to the 'Calculate docker image' step. Every value derived from inputs (the docker-image, docker-tag and custom-tag-prefix outputs) is now cleaned into its own variable before it is written to $GITHUB_OUTPUT. The cleaning runs on variables that already hold the values, not wrapped around a command, so a failing command still stops the step.
- Retry helper: in the 'Check if image should be built' and 'Login to ECR' steps, the helper now passes its arguments through as "$@" instead of an unquoted $*.
- Build step: the image name is now quoted when it is passed to awk (via printf '%s\n'), and the build script path (inputs.docker-build-script) is quoted as a single value. One behaviour change: a docker-build-script value containing spaces (for example a script plus extra flags) used to be split into separate words and is now run as one path. The input is described as a single script path, so this should not matter in practice.
- Pinning: nick-fields/retry is pinned to 7152eba30c6575329ac0576536151aca5a72780e, with a # v3.0.0 comment.
I did not run the action after these changes.

