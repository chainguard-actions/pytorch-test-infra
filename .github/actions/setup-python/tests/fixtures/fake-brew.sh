#!/bin/sh
# Fake Homebrew: logs invocations and reports FAKE_PREFIX for `brew --prefix`.
echo "brew $*" >> "$FAKE_LOG"
case "$1" in
  --prefix) echo "$FAKE_PREFIX" ;;
esac
exit 0
