<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261109-192709** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' (composite run block) writes input-derived values to $GITHUB_OUTPUT with no `printf '%s' ... | tr -d '\n\r'` sanitization. Examples: `echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"` (DOCKER_IMAGE_NAME comes from inputs.docker-image-name), `echo "docker-tag=${DOCKER_TAG}"` (derived from the image name or from inputs.custom-tag-prefix), `echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"` (built from inputs.docker-registry, inputs.repo-name and github.event.repository.name), and `echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}"`. A newline in any of these values can inject extra step outputs, which later steps use in `if:` conditions and for the docker build/push.

Locations:

- `action.yml:93`
- `action.yml:103`
- `action.yml:104`
- `action.yml:116`
- `action.yml:117`
- `action.yml:118`

### script-injection (severity: high)

Rule (b): unquoted expansion of workflow-controlled env vars in the shell script that the 'Build docker image' step passes to nick-fields/retry `command:`, which runs it in bash just like a run block. `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)` expands DOCKER_IMAGE (a step output built from inputs) without quotes. `${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..." -t "${DOCKER_IMAGE}"` runs the unquoted inputs.docker-build-script value as a command, so the value is split into words and glob-expanded before it runs.

Locations:

- `action.yml:247`
- `action.yml:249`

### unpinned-uses (severity: high)

A composite action step references an action by tag instead of a full 40-character commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:235`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

All changes are in action.yml.

1. Output injection: in the 'Calculate docker image' step, every value written to $GITHUB_OUTPUT (docker-image, docker-tag, custom-tag-prefix) is now passed through printf '%s' ... | tr -d '\n\r' first, so a newline can't add extra outputs. Each input is copied into a variable on its own line, so a failing command can't be hidden.

2. Script injection: in the 'Build docker image' retry command, I put double quotes around the DOCKER_IMAGE prefix-strip inside the echo, and around "${DOCKER_BUILD_SCRIPT}" so it runs as one path. Its value is a single script path (default ./build.sh), so quoting doesn't change how a normal value behaves. One side effect: a value containing spaces or glob characters, which upstream would have split or expanded, now runs as one literal path.

3. Pinning: nick-fields/retry is now pinned to 7152eba30c6575329ac0576536151aca5a72780e # v3.0.0, the commit SHA I looked up for that tag.

I haven't run the action or re-run the analysis on these edits.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

In action.yml, the retry helper in both the 'Check if image should be built' step and the 'Login to ECR' step used an unquoted $*. I changed it to "$@" in both places, so the docker-registry value now reaches login as a single argument, without being split on whitespace or glob-expanded. For the normal registry value, which has no spaces, retry and login behave as before. Nothing was run or tested after the change.

