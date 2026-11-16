#!/bin/bash
# Fixture script executed by the action under test.
echo "script ran" > "${MARKER_FILE}"
echo "FROM_ENV=${FROM_ENV:-unset}" >> "${MARKER_FILE}"
echo "PWD=$(pwd)" >> "${MARKER_FILE}"
