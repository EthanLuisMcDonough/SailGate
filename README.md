# SailGate

SailGate is a Hardware Description Language embedded inside the
[ParaSail programming language](https://github.com/parasail-lang/parasail).
It uses ParaSail's reflection library to lower user-defined modules into
VHDL entities.


## Installation

1. Install the ParaSail programming language on your system. As
of right now, you need to build it from source in order to get
an up-to-date version of the interpreter. You'll need to set
the `PARASAIL_ROOT` environment variable to the ParaSail directory.
```sh
$ git clone https://github.com/parasail-lang/parasail
$ cd parasail
$ make
$ pwd
/your-dir-abs/parasail
$ export PARASAIL_ROOT=$(pwd)
```

2. Download the SailGate repository and mark the `sailgate.sh`
as executable. Then, add `./bin` to your PATH.
```sh
$ git clone https://github.com/EthanLuisMcDonough/SailGate
$ cd SailGate
$ chmod +x ./bin/sailgate.sh
$ export PATH="/your-dir-abs/SailGate/bin:$PATH"
```

3. Invoke SailGate's driver by calling `sailgate.sh` with your
SailGate design files.
```sh
$ sailgate.sh examples/counter_2bit.psl -o out_dir
$ ls out_dir
Entity_Mux_4.vhd
$ cat out_dir/Entity_Mux_4.vhd
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
...
```

## Testing

Directions for running SailGate's test suite are in the
[tests](./tests) directory.
