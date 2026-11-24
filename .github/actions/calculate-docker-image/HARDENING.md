<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261123-205410** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' (id: calculate-image) writes values that come from workflow inputs to $GITHUB_OUTPUT without first running them through `printf '%s' ... | tr -d '\n\r'`. The values are DOCKER_IMAGE_NAME (inputs.docker-image-name), DOCKER_REGISTRY (inputs.docker-registry), REPO_NAME (inputs.repo-name / github.event.repository.name), CUSTOM_TAG_PREFIX (inputs.custom-tag-prefix, or text taken from the image name) and DOCKER_TAG, which is built from those values. Affected lines: `echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"`, `echo "docker-tag=${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"`, `echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"` and `echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" >> "${GITHUB_OUTPUT}"`. A value containing a newline can add extra step outputs, such as a forged docker-image.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### unpinned-uses (severity: high)

A composite step references an action by a version tag instead of a full 40-character commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:234`

### script-injection (severity: high)

Rule (b), unquoted expansion. In step 'Check if image should be built', the helper `retry () { $*  || (sleep 1 && $*) || (sleep 2 && $*) }` expands its arguments unquoted with `$*`. It is called as `retry login "${DOCKER_REGISTRY}"`, so the quoting is lost and DOCKER_REGISTRY (inputs.docker-registry) is split on whitespace and glob-expanded again. Using "$@" fixes this.

Locations:

- `action.yml:141`

### script-injection (severity: high)

Rule (b), unquoted expansion. Step 'Login to ECR' has the same `retry () { $*  || (sleep 1 && $*) || (sleep 2 && $*) }` helper. It re-expands the input-derived DOCKER_REGISTRY (inputs.docker-registry) unquoted through `$*` when called as `retry login "${DOCKER_REGISTRY}"`. Using "$@" fixes this.

Locations:

- `action.yml:212`

### script-injection (severity: high)

Rule (b), unquoted expansion. Step 'Build docker image' runs a shell script through the `command:` input of nick-fields/retry, and that script expands workflow-controlled env vars unquoted. One line is `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)`, where DOCKER_IMAGE comes from step outputs built from inputs. Another is `${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..." -t "${DOCKER_IMAGE}"`, where inputs.docker-build-script is expanded unquoted as the command to run. Both should be double-quoted.

Locations:

- `action.yml:246`
- `action.yml:248`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, unpinned-uses, script-injection

**Notes:**

I fixed all three findings in action.yml. I have not run the action afterwards.

- **github-env-injection:** I added a `sanitize()` helper (`printf '%s' "$1" | tr -d '\n\r'`) to the 'Calculate docker image' step. Every write of docker-image, docker-tag and custom-tag-prefix to GITHUB_OUTPUT now goes through it. Each value is captured into its own variable first, never by putting a command substitution inside another function call.
- **unpinned-uses:** I pinned `nick-fields/retry` to commit `7152eba30c6575329ac0576536151aca5a72780e` (the v3.0.0 tag), keeping `# v3.0.0` as a comment.
- **script-injection, `retry` helper:** In the 'Check if image should be built' and 'Login to ECR' steps, the helper now passes its arguments on with `"$@"` instead of `$*`, so the registry name stays one argument.
- **script-injection, 'Build docker image' step:** The image name is now expanded double-quoted through `printf '%s\n'` before it goes to awk. The build script is now called as `"${DOCKER_BUILD_SCRIPT}"`, one quoted word.

One behaviour change: because the build script is now quoted, `docker-build-script` is treated as a single path (it defaults to `./build.sh`). Previously, a value with extra words such as `./build.sh --flag` was split into a script plus arguments; now the whole string is taken as one file name. Any caller relying on that would need to change.

