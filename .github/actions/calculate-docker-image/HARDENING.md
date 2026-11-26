<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261125-223308** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' writes values derived from untrusted inputs to $GITHUB_OUTPUT without the `printf '%s' ... | tr -d '\n\r'` sanitization step. The inputs are inputs.docker-image-name, inputs.docker-registry, inputs.repo-name / github.event.repository.name and inputs.custom-tag-prefix. The writes are: `echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"` (lines 92, 103), `echo "docker-tag=${DOCKER_TAG}"` (lines 102, 115; DOCKER_TAG comes from DOCKER_IMAGE_NAME or CUSTOM_TAG_PREFIX), `echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"` (line 116) and `echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}"` (line 117). A newline in any of these values can inject extra step outputs.

Locations:

- `action.yml:92`
- `action.yml:103`
- `action.yml:116`
- `action.yml:117`

### script-injection (severity: high)

Rule (b), steps 'Check if image should be built' and 'Login to ECR': the helper `retry () { $*  || (sleep 1 && $*) || (sleep 2 && $*) }` is called as `retry login "${DOCKER_REGISTRY}"`. Inside the helper, `$*` re-expands DOCKER_REGISTRY (from inputs.docker-registry) without quotes, so the value is word-split and glob-expanded. The fix is to use `"$@"`.

Locations:

- `action.yml:141`
- `action.yml:212`

### script-injection (severity: high)

Rule (b), step 'Build docker image' (a shell script passed through nick-fields/retry's `command:`): `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)` expands DOCKER_IMAGE (a step output derived from inputs) without quotes. Also, `${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..." -t "${DOCKER_IMAGE}"` expands inputs.docker-build-script without quotes and runs it as a command.

Locations:

- `action.yml:246`
- `action.yml:248`

### unpinned-uses (severity: high)

The composite step uses a mutable tag instead of a full 40-character commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:234`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

All four findings are fixed, in hardened/action/action.yml (the action's only file). Nothing has been run or tested yet.

- github-env-injection: the 'Calculate docker image' step now has a small sanitize() helper, `printf '%s' "$1" | tr -d '\n\r'`. Each value is cleaned into its own variable just before it is written to GITHUB_OUTPUT. This covers both docker-image writes, both docker-tag writes, the registry/repo/name:tag image string and custom-tag-prefix. Values without newlines come out unchanged.
- script-injection, retry helper: in both 'Check if image should be built' and 'Login to ECR', `$*` became `"$@"`. The registry value is no longer split into words or matched as a filename pattern.
- script-injection, build step: `echo ${DOCKER_IMAGE#...}` became `printf '%s\n' "${DOCKER_IMAGE#...}"`, which is quoted. The build script is now run as `"${DOCKER_BUILD_SCRIPT}"`. I treated docker-build-script as a single path because the action already checks it with `-f "${DOCKER_BUILD_DIR}/${DOCKER_BUILD_SCRIPT}"`, which only works for one file name. One behaviour change: a caller who put extra arguments in that input (e.g. './build.sh --flag') would now break, though the `-f` check probably already rejected such values.
- unpinned-uses: nick-fields/retry is pinned to 7152eba30c6575329ac0576536151aca5a72780e # v3.0.0, the commit SHA looked up for that tag.

