# LLVM-LIT configuration file for SailGate integration tests

import os
import lit.formats

test_dir = os.path.dirname(__file__)
shared_dir = os.path.join(test_dir, "shared")
base_dir = os.path.abspath(os.path.join(test_dir, os.pardir))

psrun_script = os.path.join(base_dir, "psrun.py")
sailgate_config = os.path.join(base_dir, "sailgate.json")
builder_config = os.path.join(base_dir, "builder.json")
stub_entry = os.path.join(shared_dir, "stub.psl")
driver_script = os.path.join(base_dir, "sailgate.sh")

# TODO: allow FileCheck location to be specified.
#       Right now, the tests assume FileCheck is in path

config.name = "SailGate"
config.suffixes = [".psi", ".psl"]
config.excludes = ["shared"]
config.test_source_root = test_dir
config.test_format = lit.formats.ShTest()

suffix = " %s > %t 2>&1"

# %sailgate_typecheck: Runs check for simple type-based tests.
#                      These tests exist to check how RTL types
#                      can be used
config.substitutions.append(("%sailgate_typecheck", "python3 " + psrun_script +
                             " " + sailgate_config + " --cmd Test -f " + stub_entry +
                             " " + suffix))

# %sailgate_check: Runs FileCheck on generated temp file
config.substitutions.append(("%sailgate_check", "FileCheck %s " +
                             "--input-file %t"))

# %sailgate_builder: Runs ParaSail file with builder library
config.substitutions.append(("%sailgate_builder", "python3 " + psrun_script +
                             " " + builder_config + " --cmd Test -f " + suffix))

# %sailgate: Runs driver with test file and checks output
config.substitutions.append(("%sailgate", driver_script + suffix))
