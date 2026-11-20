#!/bin/sh
# Fake venv python: logs invocations (e.g. "-m pip install -r file").
echo "venv-python $*" >> /tmp/venv-python.log
exit 0
