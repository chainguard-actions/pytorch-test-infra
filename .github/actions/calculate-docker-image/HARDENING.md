<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261103-202628** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

The 'Calculate docker image' step writes values built from inputs to $GITHUB_OUTPUT without first passing them through `printf '%s' ... | tr -d '\n\r'`. The values come from inputs.docker-image-name, inputs.custom-tag-prefix, inputs.docker-registry and inputs.repo-name/github.event.repository.name, routed through the DOCKER_IMAGE_NAME, CUSTOM_TAG_PREFIX, DOCKER_REGISTRY and REPO_NAME env vars. The unsanitized writes are: `echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"` (lines 92 and 103), `echo "docker-tag=${DOCKER_TAG}"` (lines 102 and 115; DOCKER_TAG is derived from DOCKER_IMAGE_NAME or CUSTOM_TAG_PREFIX), `echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"` (line 116) and `echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}"` (line 117). A value containing a newline can inject extra step outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### script-injection (severity: high)

Rule (b), unquoted expansion of workflow-controlled data. In the 'Build docker image' step, the shell script passed to nick-fields/retry through `command:` (run with bash) has two unquoted expansions. Line 246: `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk -F '[:,]' '{print $1}')`. DOCKER_IMAGE comes from a step output derived from inputs and is expanded without quotes. Line 248: `${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..." -t "${DOCKER_IMAGE}"`. DOCKER_BUILD_SCRIPT comes from inputs.docker-build-script and is expanded without quotes, so it is word-split and glob-expanded before being run as a command.

Locations:

- `action.yml:246`
- `action.yml:248`

### unpinned-uses (severity: high)

A composite step references an action by tag, not by a full commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:234`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

I fixed all three findings in action.yml. I didn't run the action, so none of this has been tested yet.

- github-env-injection: In the 'Calculate docker image' step, every value written to $GITHUB_OUTPUT (docker-image, docker-tag, custom-tag-prefix) now goes through printf '%s' ... | tr -d '\n\r' first, so a newline in an input can no longer add extra step outputs.
- script-injection: In the 'Build docker image' retry command, the DOCKER_IMAGE prefix-strip is now quoted (printf '%s\n' "${DOCKER_IMAGE#...}"). "${DOCKER_BUILD_SCRIPT}" is quoted too. That is safe because the first step requires the input to be a single file path (it checks -f on "${DOCKER_BUILD_DIR}/${DOCKER_BUILD_SCRIPT}" before any build runs).
- unpinned-uses: Pinned nick-fields/retry to 7152eba30c6575329ac0576536151aca5a72780e (v3.0.0); I looked up the SHA rather than guessing it.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

Replaced the unquoted `$*` with quoted "$@" in the `retry` helper in both 'Check if image should be built' and 'Login to ECR' steps of action.yml, so the docker-registry input is passed as a single argument and is no longer word-split or glob-expanded.

