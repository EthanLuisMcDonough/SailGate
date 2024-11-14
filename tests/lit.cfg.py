# LLVM-LIT configuration file for SailGate integration tests

import os
import lit.formats

test_dir = os.path.dirname(__file__)
base_dir = os.path.abspath(os.path.join(test_dir, os.pardir))
driver_script = os.path.join(base_dir, "sailgate.sh")

# TODO: allow FileCheck location to be specified.
#       Right now, the tests assume FileCheck is in path

config.name = "SailGate"
config.suffixes = [".psi", ".psl"]
config.test_source_root = test_dir
config.test_format = lit.formats.ShTest()
config.substitutions.append(("%sailgate_check", "echo \"\" | " + driver_script + " %s 2>&1 | FileCheck %s"))
