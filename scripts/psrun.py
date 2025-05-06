#!/usr/bin/env python3
import argparse
import pathlib
import psutil

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

config = psutil.load_config(cli_args.config_file)

if cli_args.nocmd and (cli_args.args or cli_args.cmd):
    psutil.fatal_error("--nocmd cannot be used with --args or --cmd")
if cli_args.cmd is not None:
    config.command = cli_args.cmd
if cli_args.nocmd:
    config.command = None
sources = [] if cli_args.files is None else cli_args.files
psutil.run_parasail(config, cli_args.config_file, sources,
                    cli_args.debug, cli_args.stdout)
