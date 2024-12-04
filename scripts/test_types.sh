#!/usr/bin/env bash

# Modified version of driver for testing RTL types.
# This script doesn't actually invoke the driver,
# it's meant for checking for compile time type errors

ROOT=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd);
GATHERER="$ROOT/psc_list_gather.sh"

echo "$ROOT/../src"
SOURCE_FILES=( $(sh "$GATHERER" "$ROOT/../src") )

yes exit | interp.csh "${SOURCE_FILES[@]}" "$@"
