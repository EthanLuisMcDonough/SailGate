# An Introduction to SailGate

## Defining Entities

All SailGate designs are composed of entities. Entities are
logical units that contain both structure and behavior. Entities
in SailGate are represented by ParaSail module definitions. The
following illustrates the structural definition of a sample SailGate
entity:

```
import SailGate::Prelude::*, *;

interface My_Entity<> is
	const Output_Val_1 : Logic;
	const Output_Val_2 : Logic;

	func Run(Input_Val_1 : Logic;
		Input_Val_2 : Logic) -> My_Entity;
end interface My_Entity
```

This part of the entity definition is analogous to the VHDL
"entity" port definition. A SailGate entity's inputs are defined
by its "Run" function's parameters and its outputs are defined by
its constant fields. `My_Entity`'s inputs are `Input_Val_1` and
`Input_Val_2`. Its outputs are `Output_Val_1` and `Output_Val_2`.
Inputs and outputs can only consist of RTL type found in SailGate's
prelude package. These types include `Logic`, `Vec`, `UVec`, and
`IVec`.

## RTL Types

SailGate's RTL types are special ParaSail type definitions located
in the `SailGate::Prelude` package. The `Logic` type represents a
logical bit (0 or 1) and `Vec<N>` represents an array of N bits.
`UVec<N>` and `IVec<N>` represent arrays of bits that are interpreted
as unsigned and signed integers of length N respectively. Each of
these types map to a synthesizable VHDL type.

| VHDL      | SailGate                           |
| --------- | ---------------------------------- |
| `Logic`   | `STD_LOGIC`                        |
| `Vec<N>`  | `STD_LOGIC_VECTOR(N - 1 downto 0)` |
| `UVec<N>` | `UNSIGNED(N - 1 downto 0)`         |
| `IVec<N>` | `SIGNED(N - 1 downto 0)`           |

Vector types are zero-indexed. Their lowest index is zero and
their upper index is N - 1. This means that a type `Vec<4>` would
have indexes that range from zero to three.

For port definitions with a vector type (`Vec`, `UVec`, and `IVec`),
a special "Align" annotation can be added to specify the range and
direction. This align clause is only usable inside input/output
definitions in entities.

```
interface My_Entity<> is
	{Align(#up, 3)} const Out : Vec<3>;
	func Run({Align(Offset => 2)} In : Vec<2>) -> My_Entity;
end interface My_Entity
```

In the above example, `Out` would have the VHDL type
`STD_LOGIC_VECTOR(3 to 5)` and `In` would have the type
`STD_LOGIC_VECTOR(3 downto 2)`.

## Defining Entity Behavior

While the `interface` portion of an entity defines the entity's
inputs and outputs, the `class` portion defines how the entity
computes its outputs. An entity's behavior is defined inside the
`Run` method:

```
class My_Entity is
exports
	func Run(Input_Val_1 : Logic;
		Input_Val_2 : Logic) -> My_Entity
	is
		return (Output_Val_1 => Input_Val_1 and Input_Val_2,
			Output_Val_2 => Input_Val_1 or Input_Val_2);
	end func Run`
end My_Entity
```

Output values are assigned by returning an object instance that
sets each output field defined in the entity. The example above
sets `Output_Val_1` to the logical and result of `Input_Val_1`
and `Input_Val_2`. It also sets `Output_Val_2` to the logical or
of `Input_Val_1` and `Input_Val_2`. Each "Run" method is expected
to contain exactly one return statement that returns an entity that
was constructed using ParaSail's module instantiation syntax.

## Combinational logic

SailGate supports a variety of operators that allow users to specify
combinational logic.

| Operator               | Class            | Arity  | Usage                                                                                                                                              |
| ---------------------- | ---------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `not`                  | Bitwise          | Unary  | Bitwise NOT                                                                                                                                        |
| `and`                  | Bitwise          | Binary | Bitwise AND                                                                                                                                        |
| `or`                   | Bitwise          | Binary | Bitwise OR                                                                                                                                         |
| `xor`                  | Bitwise          | Binary | Bitwise XOR                                                                                                                                        |
| `==`                   | Comparison       | Binary | Equality                                                                                                                                           |
| `!=`                   | Comparison       | Binary | Inequality                                                                                                                                         |
| `>=`                   | Comparison       | Binary | Greater than or equal to                                                                                                                           |
| `<=`                   | Comparison       | Binary | Less than or equal to                                                                                                                              |
| `>`                    | Comparison       | Binary | Greater than                                                                                                                                       |
| `<`                    | Comparison       | Binary | Less than                                                                                                                                          |
| `>>`                   | Bitwise          | Binary | Right shift                                                                                                                                        |
| `<<`                   | Bitwise          | Binary | Left shift                                                                                                                                         |
| `\|`                   | Vector operation | Binary | Value concatenation. `Vec<3> \| Vec<2>` \= `Vec<5>`. Individual logic values can also be added to vectors or other logic values to create vectors. |
| `[N]`                  | Vector operation | Binary | Vector indexing. N must be a constant integer within vector bounds. Indexing can be used to read or modify a value.                                |
| `Range<A, B>::Slice()` | Vector operation | 3      | Vector slicing. A and B must be constant integers within vector bounds. The returned value is a vector of length \|A \- B\| \+ 1\.                 |

| Type               | Supported operators                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------ |
| `Logic`            | `not, and, or, xor, ==, !=, >=, <=, >, <, \|`                                              |
| `Vec<N>`           | `not, and, or, xor, ==, !=, >=, <=, >, <, \|, [N], Range<A, B>::Slice`                     |
| `UVec<N>, IVec<N>` | `not, and, or, xor, ==, !=, >=, <=, >, <, \|, +, -, *, /, <<, >>, [N], Range<A, B>::Slice` |

It is important to note that comparison operators return a type
called `Rtl_Bool`. This type cannot be used as an input, output,
or register. This type is only used inside conditional expressions.

For all binary operators, both types must have a matching clock domain.
Mismatching clock domains result in a semantic error. All binary operators
except the concatenation operator mandate that both types share a length.

Vector types can be converted into other vector types `Logic_Vec`,
`To_IVec`, and `To_UVec`. These functions do not change the type's
size or clock domain.

## Wires and registers**

You can use constant variables, or wires, to store intermediate combinational
values:

```
class My_Entity is
exports
	func Run(Input_Val_1 : Logic;
		Input_Val_2 : Logic) -> My_Entity
	is
		const IV_1 := Input_Val_1 and Input_Val_2;
		const IV_2 := Input_Val_1 or Input_Val_2;
		return (Output_Val_1 => IV_1 xor IV_2,
			Output_Val_2 => IV_2 and Input_Val_1);
	end func Run
end class My_Entity
```

Registers are used for sequential logic. Registers are local mutable
variables with RTL types. Register initial values must be constant.
The previous circuit can be rewritten as:

```
class My_Entity is
exports
	func Run(Input_Val_1 : Logic;
		Input_Val_2 : Logic) -> My_Entity
	is
		var IV_1 : Logic := '0';
		var IV_2 : Logic := '0';
		IV_1 := Input_Val_1 and Input_Val_2;
		IV_2 := Input_Val_1 or Input_Val_2;
		return (Output_Val_1 => IV_1 xor IV_2,
			Output_Val_2 => IV_2 and Input_Val_1);
	end func Run
end class My_Entity
```

Both circuits behave the same, but their generated VHDL differs
slightly.

## Clock domains

Clock domains allow the developer to abstract over the process of
managing clock signals. They are statically checked "regions" that
are tied to types. Each RTL type has an optional clock domain parameter
(e.g. `Logic<D>`, `Vec<2, G>`) that is set to `Async` by default.
SailGate uses this clock domain to statically check for conflicts that
could cause metastability issues.

Clock domains are defined as entity module parameters. SailGate supports
four different clock domain types: `Clock`, `Reset`, `Clk_Rst_En`, and
`Async`. Multiple clock domains can be defined in a single entity as
long as each clock domain has a separate name.

| Clock domain | Description                                                                          | Definition                   |
| ------------ | ------------------------------------------------------------------------------------ | ---------------------------- |
| Async        | A domain that doesn't have a clock                                                   | `D : Domain`                 |
| Clock        | A domain with a clock signal                                                         | `D : Domain {Clock(D)}`      |
| Reset        | A domain with a clock and an active high reset signal                                | `D : Domain {Reset(D)}`      |
| Enable       | A domain with a clock, an active high reset signal, and an active high enable signal | `D : Domain {Clk_Rst_En(D)}` |

Fig.(10.14) shows a sequential 2-bit counter defined in SailGate.

```
interface Counter_2Bit<D : Domain {Clock(D)}> is
	const Result_Val : Vec<2, D>;
	func Run() -> Counter_2Bit;
end interface Counter_2Bit

class Counter_2Bit is
exports`  
	func Run() -> Counter_2Bit is
		var Counter : UVec<2, D> := 0;
		Counter := Counter + 1;
		return (Result_Val => Logic_Vec(Counter));
	end func Run
end class Counter_2Bit
```
The parameter type `D : Domain {Clock(D)}` specifies that this entity
accepts a clock domain that contains at least a clock signal. Domains
with resets and enables can be supplied to this domain, but async clock
domains can't be used here. Counter is a register that maintains its
value throughout the circuit's lifecycle. If this domain was a clock reset
domain, `Counter` would be reset whenever the reset signal was enabled.
Sequential operations that are bound to clock domains, like
`Counter := Counter + 1`, are moved inside their respective processes.
A side by side comparison between SailGate and the generated VHDL can
be seen here:

![SailGate to VHDL mapping](./images/vhdl_2bit_counter_mapping-dark.svg#gh-dark-mode-only)
![SailGate to VHDL mapping](./images/vhdl_2bit_counter_mapping.svg#gh-light-mode-only)

The `Sync` function is used to convert entities from an asynchronous
domain to any clock domain. `Unsafe_Cast` is used to convert a value
with a clock domain to an asynchronous value and should only be used
when the developer wants to deliberately cross clock domains.

## Sequential control flow

ParaSail if statements and case/of statements are lowered into VHDL by
SailGate. These constructs operate identically to how they do in ParaSail,
but case/of statements expect the selector to be wrapped in a call to
`Switch`:

```
`class Mux_4 is`  
`exports`  
	`func Run(Select : Vec<2, Dom>;`  
			`A : Vec<4, Dom>; B : Vec<4, Dom>;`  
			`C : Vec<4, Dom>; D : Vec<4, Dom>) -> Mux_4`  
	`is`  
			`var Out_Val : Vec<4, Dom> := 0;`

			`case Switch(Select) of`  
					`["00"] =>`  
						`Out_Val := A;`  
					`["01"] =>`  
						`Out_Val := B;`  
					`["10"] =>`  
						`Out_Val := C;`  
					`["11"] =>
						Out_Val := D;
			end case
			return (Output => Out_Val);
	end func Run
end class Mux_4
```

All statements inside a sequential construct must be of the same clock
domain. If they aren't, SailGate will raise a semantic error.

## Entity reuse

Entities can be called from within other entities. The following circuit
outputs '1' if and only if its internal counter component's value is three:

```
interface Counter_User<D : Domain {Clock(D)}> is
	const Active : Logic<D>;
	func Run() -> Counter_User;
end interface Counter_User

class Counter_User is
	type Component is Counter<D>;
exports
	func Run() -> Counter_User is`  
		const Clock_Inst := Component::Run();
		var Result : Logic<D>;

		if Clock_Inst.Value == "11" then
			Result := '1';
		else
			Result := '0';
		end if

		return (Active => Result);
	end func Run
end class Counter_User
```

An entity can only be instantiated through its respective "Run" function.
Additionally, all entity instantiations must be constant. Variable entity
instantiations are not allowed.

## Invoking SailGate

You can invoke the SailGate driver by using the `sailgate.sh` script found
in [`bin` directory](../bin/sailgate.sh). Feed this script all of your SailGate
source files and specify the output directory using the `-o` command line flag:

```console
$ sailgate.sh file1.psl file2.psl -o out_dir
```
