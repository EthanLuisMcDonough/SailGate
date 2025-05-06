#!/usr/bin/env python3
import argparse
import pathlib
import psutil
import os

script_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.dirname(script_dir)
config_dir = os.path.join(project_dir, "project_configs")
main_config = os.path.join(config_dir, "sailgate.json")

config = psutil.load_config(main_config)

arg_parser = argparse.ArgumentParser(prog="SailGate driver",
    description="Compile SailGate designs to RTL")
arg_parser.add_argument("sources", nargs='*', type=pathlib.Path,
                        help="SailGate source files")
arg_parser.add_argument("--output", "-o", type=pathlib.Path, default=".",
                        help="Directory to output the design files to")

cli_args = arg_parser.parse_args()

if str(cli_args.output) != "-":
    if not cli_args.output.exists():
        os.mkdir(cli_args.output)
    elif not cli_args.output.is_dir():
        psutil.fatal_error("output path \"" + str(cli_args.output) +
                        "\" is not a directory")

config.args = [cli_args.output, os.sep]

psutil.run_parasail(config, main_config, cli_args.sources)
