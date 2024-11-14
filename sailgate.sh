#!/usr/bin/env bash

# Minimal SailGate driver script
# assumes interp.csh and parasail_main are both in path

ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

interp.csh "$ROOT/src/driver.psi" "$ROOT/src/types.psi" \
    "$ROOT/src/extractor.psi" "$ROOT/src/*.psl" "$@" \
    -command Main
