# LLVM-LIT configuration file for SailGate integration tests

import os
import lit.formats

test_dir = os.path.dirname(__file__)
shared_dir = os.path.join(test_dir, "Shared")
base_dir = os.path.abspath(os.path.join(test_dir, os.pardir))
script_dir = os.path.join(base_dir, "scripts")

driver_script = os.path.join(base_dir, "sailgate.sh")
type_script = os.path.join(script_dir, "test_types.sh")
builder_script = os.path.join(script_dir, "test_vhdl_builder.sh")

# TODO: allow FileCheck location to be specified.
#       Right now, the tests assume FileCheck is in path

config.name = "SailGate"
config.suffixes = [".psi", ".psl"]
config.excludes = ["Shared"]
config.test_source_root = test_dir
config.test_format = lit.formats.ShTest()

suffix = " %s > %t 2>&1"
fake_dom = os.path.join(shared_dir, "fake_domain.psi")

# %sailgate_typecheck: Runs check for simple type-based tests.
#                      These tests exist to check how RTL types
#                      can be used
config.substitutions.append(("%sailgate_typecheck", type_script + suffix))


# %sailgate_check: Runs FileCheck on generated temp file
config.substitutions.append(("%sailgate_check", "FileCheck %s " +
                             "--input-file %t"))

# %sailgate_builder: Runs ParaSail file with builder library
config.substitutions.append(("%sailgate_builder", builder_script + suffix))

# %sailgate: Runs driver with test file and checks output
config.substitutions.append(("%sailgate", driver_script + suffix))
