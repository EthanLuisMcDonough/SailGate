#!/usr/bin/env bash

# Gathers ParaSail files from a project that uses
# psc_list.txt

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

read_dir $1;

for value in "${HEADER_FILES[@]}"; do
    echo $value;
done

for value in "${SOURCE_FILES[@]}"; do
    echo $value;
done
