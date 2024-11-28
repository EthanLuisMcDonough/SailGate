# LLVM-LIT configuration file for SailGate integration tests

import os
import lit.formats

test_dir = os.path.dirname(__file__)
shared_dir = os.path.join(test_dir, "Shared")
base_dir = os.path.abspath(os.path.join(test_dir, os.pardir))
driver_script = os.path.join(base_dir, "sailgate.sh")

# TODO: allow FileCheck location to be specified.
#       Right now, the tests assume FileCheck is in path

config.name = "SailGate"
config.suffixes = [".psi", ".psl"]
config.excludes = ["Shared"]
config.test_source_root = test_dir
config.test_format = lit.formats.ShTest()

dbg_console_prefix = "echo \"\" | "
filecheck_suffix = " %s 2>&1 | FileCheck %s"
fake_dom = os.path.join(shared_dir, "fake_domain.psi")

# %sailgate_typecheck: Runs check for simple type-based tests.
#                      These tests exist to check how RTL types
#                      can be used
config.substitutions.append(("%sailgate_typecheck", dbg_console_prefix +
                             driver_script + " " + fake_dom +
                             filecheck_suffix))

# %sailgate_check: Runs driver with test file and checks output
config.substitutions.append(("%sailgate_check", dbg_console_prefix +
                             driver_script + filecheck_suffix))
