<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261109-232755** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' (id: calculate-image) writes values from workflow inputs to $GITHUB_OUTPUT without first stripping newlines with `printf '%s' ... | tr -d '\n\r'`. The values come from inputs.docker-image-name, inputs.custom-tag-prefix, inputs.docker-registry and inputs.repo-name/github.event.repository.name, passed in through env. The unsanitized writes are: `echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"` (lines 92 and 103), `echo "docker-tag=${DOCKER_TAG}"` where DOCKER_TAG comes from DOCKER_IMAGE_NAME or CUSTOM_TAG_PREFIX (lines 102 and 115), `echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"` (line 116) and `echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}"` (line 117). A value containing a newline could add extra outputs, such as a fake docker-image.

Locations:

- `action.yml:92`
- `action.yml:103`
- `action.yml:116`
- `action.yml:117`

### script-injection (severity: high)

Rule (b), 'Check if image should be built' step: the retry helper runs `$*  || (sleep 1 && $*) || (sleep 2 && $*)` with $* unquoted. It is called as `retry login "${DOCKER_REGISTRY}"`, so inputs.docker-registry is re-expanded without quotes. The value then gets split on whitespace and glob-expanded. Use "$@" instead.

Locations:

- `action.yml:141`

### script-injection (severity: high)

Rule (b), 'Login to ECR' step: the same retry helper runs `$*  || (sleep 1 && $*) || (sleep 2 && $*)` with $* unquoted, so DOCKER_REGISTRY (from inputs.docker-registry) is re-expanded without quotes. Use "$@" instead.

Locations:

- `action.yml:212`

### script-injection (severity: high)

Rule (b), 'Build docker image' step: the bash script passed to nick-fields/retry as `command:` expands workflow-controlled data without quotes. On line 246, `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)` leaves the DOCKER_IMAGE step output (built from inputs) unquoted. On line 248, `${DOCKER_BUILD_SCRIPT} ...` runs inputs.docker-build-script unquoted. Quote both expansions, e.g. `echo "${DOCKER_IMAGE#...}"` and `"${DOCKER_BUILD_SCRIPT}"`.

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

I fixed all five findings in action.yml. I haven't run the action since the edits, so these changes are untested.

- **Output injection (Calculate docker image step):** I added a `sanitize()` helper that runs `printf '%s' "$1" | tr -d '\n\r'`. Every value written to GITHUB_OUTPUT (docker-image, docker-tag, custom-tag-prefix) is now stored in a variable after sanitizing and only then written. A value containing a newline can no longer add fake outputs.
- **Retry helper (Check if image should be built and Login to ECR steps):** `$*` is replaced with `"$@"` in both steps, so the docker-registry input is no longer split on spaces or expanded as a wildcard pattern.
- **Build docker image step:**
  - The expansion inside the `IMAGE_NAME=$(echo ...)` line is now quoted.
  - `${DOCKER_BUILD_SCRIPT}` is now quoted, so it is run as a single path. Earlier in the script it is already checked as one file path. One change in behaviour: a docker-build-script value with extra arguments after the path would now fail. The default `./build.sh` is unaffected.
- **Unpinned action:** `nick-fields/retry@v3.0.0` is now pinned to the looked-up SHA `7152eba30c6575329ac0576536151aca5a72780e`, with `# v3.0.0` kept as a comment.

