#!/bin/sh
# Fake Homebrew: logs invocations and reports a fake prefix.
echo "brew $*" >> /tmp/brew.log
case "$1" in
  --prefix) echo /tmp/fakebrew ;;
esac
exit 0
