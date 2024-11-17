#!/usr/bin/env bash

# Minimal SailGate driver script
# assumes interp.csh is in path

ROOT=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd );
HEADER_FILES=();
SOURCE_FILES=();

read_dir() {
    if [[ $1 == *.psi ]]; then
        HEADER_FILES+=("$1");
    else
        for item in $(cat "$1/psc_list.txt"); do
            read_dir "$1/$item";
        done
        SOURCE_FILES+=("$1/*.psl");
    fi
} 

read_dir "$ROOT/src"

interp.csh "${HEADER_FILES[@]}" "${SOURCE_FILES[@]}" "$@" -command Main
