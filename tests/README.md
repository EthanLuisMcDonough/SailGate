# Running integrated tests

SailGate's integrated tests use LLVM LIT. You can install `lit`
and `FileCheck` by installing LLVM or an LLVM toolchain. Once you
have both in your PATH, run like so:

```sh
lit ./tests
```
