#!/usr/bin/env bash

# Minimal SailGate driver script
# assumes interp.csh and parasail_main are both in path

ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

interp.csh "$ROOT/src/driver.psi" "$ROOT/src/prelude/prelude.psi" \
    "$ROOT/src/prelude/util.psi" "$ROOT/src/prelude/scalar.psi" \
    "$ROOT/src/prelude/vec.psi" "$ROOT/src/prelude/module.psi" \
    "$ROOT/src/sema/sema.psi" "$ROOT/src/sema/extractor.psi" \
    "$ROOT/src/prelude/*.psl" "$ROOT/src/sema/*.psl" \
    "$ROOT/src/*.psl" "$@" -command Main
