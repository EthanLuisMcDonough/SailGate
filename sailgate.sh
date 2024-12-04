#!/usr/bin/env bash

# Minimal SailGate driver script
# assumes interp.csh is in path

ROOT=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd);
GATHERER="$ROOT/scripts/psc_list_gather.sh"

SOURCE_FILES=( $(sh "$GATHERER" "$ROOT/src") )

interp.csh "${SOURCE_FILES[@]}" "$@" -command Main
