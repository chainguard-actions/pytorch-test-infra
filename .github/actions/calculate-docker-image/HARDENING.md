<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261027-001733** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' writes values taken from inputs to $GITHUB_OUTPUT without first stripping newlines with printf '%s' ... | tr -d '\n\r'. The values come from inputs.docker-image-name, inputs.docker-registry, inputs.repo-name / github.event.repository.name and inputs.custom-tag-prefix, either directly or through DOCKER_TAG and CUSTOM_TAG_PREFIX. Examples: echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}" (lines 92, 103), echo "docker-tag=${DOCKER_TAG}" (lines 102, 115), echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" (line 116), echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" (line 117). A value containing a newline could inject extra step outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### script-injection (severity: high)

Rule (b): step 'Check if image should be built'. The retry helper runs '$*  || (sleep 1 && $*) || (sleep 2 && $*)' with $* unquoted, and it is called as 'retry login "${DOCKER_REGISTRY}"'. DOCKER_REGISTRY comes from inputs.docker-registry, so the input gets an unquoted re-expansion (word splitting and glob expansion). Use "$@" instead.

Locations:

- `action.yml:141`
- `action.yml:144`

### script-injection (severity: high)

Rule (b): step 'Login to ECR'. Same retry helper with unquoted $* ('$*  || (sleep 1 && $*) || (sleep 2 && $*)'), which re-expands the workflow-controlled DOCKER_REGISTRY (inputs.docker-registry) without quotes in 'retry login "${DOCKER_REGISTRY}"'.

Locations:

- `action.yml:212`
- `action.yml:215`

### script-injection (severity: high)

Rule (b): step 'Build docker image'. Its shell command, run by bash through nick-fields/retry, expands workflow-controlled data without quotes: 'IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)' (DOCKER_IMAGE is derived from a step output) and '${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..." -t "${DOCKER_IMAGE}"' (DOCKER_BUILD_SCRIPT comes from inputs.docker-build-script).

Locations:

- `action.yml:246`
- `action.yml:248`

### unpinned-uses (severity: high)

A composite step references an action by version tag instead of a full 40-character commit SHA: 'uses: nick-fields/retry@v3.0.0'.

Locations:

- `action.yml:234`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

I fixed all the findings in action.yml, but haven't run the action to test the changes.

- **github-env-injection:** I added a `sanitize` helper (`printf '%s' | tr -d '\n\r'`) to the 'Calculate docker image' step. Every docker-image, docker-tag and custom-tag-prefix value now goes through it, as a separate assignment, before it is written to $GITHUB_OUTPUT.
- **script-injection, retry helper:** In 'Check if image should be built' and 'Login to ECR', the retry helper now runs `"$@"` instead of the unquoted `$*`.
- **script-injection, 'Build docker image':** The image name is now computed with a quoted `printf '%s\n' "${DOCKER_IMAGE#...}"`, and the build script is called as `"${DOCKER_BUILD_SCRIPT}"`. Quoting the script matches how the action already uses it: an earlier step checks it with `-f "${DOCKER_BUILD_DIR}/${DOCKER_BUILD_SCRIPT}"`, so it has to be a single file path. A docker-build-script value that adds arguments after the path (e.g. `./build.sh --foo`) would no longer work, but it would already fail that file check.
- **unpinned-uses:** I pinned `nick-fields/retry` to the commit for v3.0.0: `7152eba30c6575329ac0576536151aca5a72780e # v3.0.0`.

