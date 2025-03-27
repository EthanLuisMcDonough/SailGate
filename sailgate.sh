#!/usr/bin/env bash

# Minimal SailGate driver script
# assumes interp.csh is in path

ROOT=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd);
python3 $ROOT/psrun.py $ROOT/sailgate.json --files "$@"
