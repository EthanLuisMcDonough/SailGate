#!/usr/bin/env bash

# Modified version of driver for testing RTL types.
# This script doesn't actually invoke the driver,
# it's meant for checking for compile time type errors

ROOT=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd);

TEST_FILE=$1
SRC_DIR="$ROOT/../src"

yes exit | interp.csh "$SRC_DIR/sailgate.psi" "$SRC_DIR/builder/builder.psi" \
    "$SRC_DIR/builder/vhdl.psi" "$SRC_DIR/builder/vhdl.psl" \
    $TEST_FILE -command Test
