<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261109-192709** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' writes values built from inputs to $GITHUB_OUTPUT without running them through `printf '%s' ... | tr -d '\n\r'` first. The values come from inputs.docker-image-name, inputs.custom-tag-prefix, inputs.docker-registry and inputs.repo-name / github.event.repository.name, passed in as DOCKER_IMAGE_NAME, CUSTOM_TAG_PREFIX, DOCKER_REGISTRY and REPO_NAME, plus DOCKER_TAG, which is derived from them. Example lines: `echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"`, `echo "docker-tag=${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"`, `echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"` and `echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" >> "${GITHUB_OUTPUT}"`. A value containing a newline can inject extra step outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### script-injection (severity: high)

Rule (b), unquoted expansion of workflow-controlled data. The `retry () { $* || (sleep 1 && $*) || (sleep 2 && $*) }` helper in steps 'Check if image should be built' and 'Login to ECR' expands its arguments unquoted. One of those arguments is "${DOCKER_REGISTRY}" (from inputs.docker-registry), so the value is word-split and glob-expanded again. Use "$@" instead.

Locations:

- `action.yml:141`
- `action.yml:212`

### script-injection (severity: high)

Rule (b), unquoted expansion of workflow-controlled data. The shell script passed to nick-fields/retry as `command:` in step 'Build docker image' (run by bash) expands untrusted variables unquoted. `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)` uses a step output and input without quotes. `${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..." -t "${DOCKER_IMAGE}"` expands inputs.docker-build-script unquoted in the command position. Quote these expansions, e.g. "${DOCKER_BUILD_SCRIPT}" and "${DOCKER_IMAGE#...}".

Locations:

- `action.yml:246`
- `action.yml:248`

### unpinned-uses (severity: high)

A composite step references an action by a mutable tag instead of a full 40-character commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:234`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

Added a sanitize() helper (printf '%s' | tr -d '\n\r') in 'Calculate docker image' step; each value is captured into a variable first and the sanitized value is what gets written to $GITHUB_OUTPUT (docker-image, docker-tag, custom-tag-prefix). Changed both retry() helpers from $* to "$@". In the nick-fields/retry command, quoted the DOCKER_IMAGE prefix-strip expansion (printf instead of echo) and quoted "${DOCKER_BUILD_SCRIPT}" in command position (consistent with the existing -f "${DOCKER_BUILD_DIR}/${DOCKER_BUILD_SCRIPT}" check that already treats it as a single path). Pinned nick-fields/retry to 7152eba30c6575329ac0576536151aca5a72780e # v3.0.0.

