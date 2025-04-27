import subprocess
import argparse
import pathlib
import shutil
import json
import glob
import sys
import os

from dataclasses import dataclass
from typing import List, Optional

PARASAIL_ROOT_ENV_NAME = "PARASAIL_ROOT"
CONFIG_CMD = "command"
CONFIG_HEADERS = "headers"
CONFIG_SRC = "sources"
CONFIG_PREFIX = "prefix"
CONFIG_ARGS = "args"

# Details read from a project config
@dataclass
class ParaSailConfig:
    headers: List[str]
    sources: List[str]
    args: Optional[List[str]] = None
    command: Optional[str] = None
    prefix: Optional[str] = None

def eprint(str):
    print("ERROR: " + str, file=sys.stderr)

def fatal_error(str):
    eprint(str)
    sys.exit(2)

# Find ParaSail root directory
def find_parasail_dir():
    if PARASAIL_ROOT_ENV_NAME in os.environ:
        return os.environ.get(PARASAIL_ROOT_ENV_NAME)

    # Find ParaSail root from parasail_main executable
    exec = shutil.which("parasail_main")
    if exec is not None:
        return os.path.realpath(os.path.join(
            os.path.dirname(exec), os.path.pardir,
            os.path.pardir))

    # Try to find ParaSail root based on interp.csh
    interp_csh = shutil.which("interp.csh")
    if interp_csh is not None:
        bin_dir = os.path.realpath(os.path.join(
            os.path.dirname(interp_csh), os.path.pardir))
        if os.path.basename(bin_dir) == "install":
            bin_dir = os.path.realpath(os.path.join(
                bin_dir, os.path.pardir))
        return bin_dir

    fatal_error("Could not find ParaSail root. Define " +
                PARASAIL_ROOT_ENV_NAME + " in your environment " +
                "or add interp.csh or parasail_main to your PATH")

def load_config(file_path: str) -> ParaSailConfig:
    with open(file_path, "r") as file:
        config = json.load(file)
        return ParaSailConfig(**config)

def run_parasail(config: ParaSailConfig, config_path: str,
                 extra_sources: List[str] = [],
                 debug: bool = False, outfile = None):
    PARASAIL_ROOT = find_parasail_dir()
    PARASAIL_LIBS = os.path.join(PARASAIL_ROOT, "lib")
    PARASAIL_STD = os.path.join(PARASAIL_LIBS, "aaa.psi")
    PARASAIL_REFLECTION_PSI = os.path.join(PARASAIL_LIBS, "reflection.psi")
    PARASAIL_REFLECTION_PSL = os.path.join(PARASAIL_LIBS, "reflection.psl")
    PARASAIL_EXE = os.path.join(PARASAIL_ROOT, "build", "bin", "parasail_main")

    full_path = os.path.realpath(config_path)
    source_dir = os.path.abspath(os.path.join(full_path, os.path.pardir))

    if config.prefix is not None:
        if os.path.isabs(config.prefix):
            source_dir = config.prefix
        else:
            source_dir = os.path.abspath(os.path.join(source_dir, config.prefix))

    sources = [PARASAIL_STD, PARASAIL_REFLECTION_PSI, PARASAIL_REFLECTION_PSL]
    for source in (config.headers + config.sources):
        sources += glob.glob(os.path.join(source_dir, source), recursive=True)

    for source in extra_sources:
        glob_sources = glob.glob(os.path.realpath(source), recursive=True)
        if not glob_sources:
            fatal_error("Could not resolve path " + str(source))
        sources += glob_sources

    if debug:
        sources += ["-debug", "on"]
    if config.command is not None:
        cmd_list = ["-command", config.command]
        if config.args is not None:
            for arg in config.args:
                cmd_list.append(arg)
        sources += cmd_list

    if outfile is not None:
        output = subprocess.run([PARASAIL_EXE] + sources, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout
        with open(outfile, "wb") as f:
            f.write(output)
    else:
        subprocess.run([PARASAIL_EXE] + sources)
