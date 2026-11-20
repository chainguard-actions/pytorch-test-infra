#!/bin/sh
# Fake Homebrew python: supports "-m venv <path>" by creating a fake venv.
echo "python $*" >> /tmp/python.log
if [ "$1" = "-m" ] && [ "$2" = "venv" ]; then
  mkdir -p "$3/bin"
  cp /tmp/fake-venv-python.sh "$3/bin/python"
  chmod +x "$3/bin/python"
fi
exit 0
