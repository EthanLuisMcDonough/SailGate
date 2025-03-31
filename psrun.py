#!/usr/bin/env python3
import subprocess
import argparse
import pathlib
import shutil
import json
import glob
import sys
import os

PARASAIL_ROOT_ENV_NAME = "PARASAIL_ROOT"
CONFIG_CMD = "command"
CONFIG_HEADERS = "headers"
CONFIG_SRC = "sources"
CONFIG_PREFIX = "prefix"
CONFIG_SEND_EXIT = "send_exit"

def eprint(str):
    print("ERROR: " + str, file=sys.stderr)

def fatal_error(str):
    eprint(str)
    sys.exit(2)

def require_prop(config, property):
    if property not in config:
        fatal_error("Propety `" + property + "` not found in config")

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

def run_parasail(config, config_path, extra_sources = [], debug = False, outfile = None):
    PARASAIL_ROOT = find_parasail_dir()
    PARASAIL_LIBS = os.path.join(PARASAIL_ROOT, "lib")
    PARASAIL_STD = os.path.join(PARASAIL_LIBS, "aaa.psi")
    PARASAIL_REFLECTION_PSI = os.path.join(PARASAIL_LIBS, "reflection.psi")
    PARASAIL_REFLECTION_PSL = os.path.join(PARASAIL_LIBS, "reflection.psl")
    PARASAIL_EXE = os.path.join(PARASAIL_ROOT, "build", "bin", "parasail_main")

    full_path = os.path.realpath(config_path)
    source_dir = os.path.abspath(os.path.join(full_path, os.path.pardir))
    if CONFIG_PREFIX in config:
        prefix = config[CONFIG_PREFIX]
        if os.path.isabs(prefix):
            source_dir = prefix
        else:
            source_dir = os.path.abspath(os.path.join(source_dir, prefix))

    sources = [PARASAIL_STD, PARASAIL_REFLECTION_PSI, PARASAIL_REFLECTION_PSL]
    for source in (config[CONFIG_HEADERS] + config[CONFIG_SRC]):
        sources += glob.glob(os.path.join(source_dir, source), recursive=True)

    for source in extra_sources:
        glob_sources = glob.glob(os.path.realpath(source), recursive=True)
        if not glob_sources:
            fatal_error("Could not resolve path " + str(source))
        sources += glob_sources

    if debug:
        sources += ["-debug", "on"]
    if CONFIG_CMD in config:
        sources += ["-command", config[CONFIG_CMD]]

    if outfile is not None:
        output = subprocess.run([PARASAIL_EXE] + sources, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout
        with open(outfile, "wb") as f:
            f.write(output)
    else:
        subprocess.run([PARASAIL_EXE] + sources)

arg_parser = argparse.ArgumentParser(prog="ParaSail config tool",
    description="Run ParaSail programs based on a specified config")

arg_parser.add_argument("config_file", type=pathlib.Path,
                        help="The path to the JSON config file")
arg_parser.add_argument("--cmd", "-c", help="Override main command")
arg_parser.add_argument("--args", "-a", help="Override command line arguments", nargs="*")
arg_parser.add_argument("--nocmd", "-nc", action="store_true", help="Don't run default command")
arg_parser.add_argument("--files", "-f", nargs='*', type=pathlib.Path,
                        help="Additional files to include in project")
arg_parser.add_argument("--debug", "-d", action="store_true",
                        help="Run ParaSail in debug mode")
arg_parser.add_argument("--stdout", "-o", type=pathlib.Path,
                        help="Pipe all output into specified file")

cli_args = arg_parser.parse_args()

with open(cli_args.config_file, "r") as file:
    config = json.load(file)
    if cli_args.nocmd and (cli_args.args or cli_args.cmd):
        fatal_error("--nocmd cannot be used with --args or --cmd")
    if cli_args.cmd is not None:
        config[CONFIG_CMD] = cli_args.cmd
    if cli_args.nocmd:
        config.pop(CONFIG_CMD, None)
    sources = [] if cli_args.files is None else cli_args.files
    require_prop(config, CONFIG_HEADERS)
    require_prop(config, CONFIG_SRC)
    run_parasail(config, cli_args.config_file, sources, cli_args.debug, cli_args.stdout)
