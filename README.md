# Static Checker

A compiler used for parsing JLite into ARM assembly code

## Directory Structure

```
├── README.md
├── doc
│   ├── LimYanPengGary_pa1_readme.md
│   └── LimYanPengGary_pa2_readme.md
├── run.sh       // bash script to run whole program
├── src
│   ├── compile.py      // Main entry point
│   ├── lex.py          // Lexer
│   ├── parse.py        // Parser - generates Parse Tree from tokens
│   ├── ast2.py         // AST generator and Type Checker
│   ├── ir3.py          // IR3 generator
│   ├── reg.py          // Register allocator
│   ├── arm.py          // ARM generator
│   └── constants.py    // Constants for ARM generator and reg allocator
└── test
│   ├── parse
│   │   ├── ... // List of assignment 1 test files
│   ├── check 
│   │   ├── ... // List of assignment 2 test files
│   ├── call.j
│   ├── call.s
│   ├── fib.j
│   ├── fib.s
│   ├── hello.j
│   ├── hello.s
│   ├── long.j
│   ├── long.s
│   ├── longer.j
│   ├── longer.s
│   ├── overload.j
│   ├── overload.s
│   ├── print.j
│   ├── print.s
│   ├── stmt.j
│   ├── stmt.s
│   ├── test_booleans.j
│   ├── test_booleans.s
│   ├── test_fields.j
│   ├── test_fields.s
│   ├── test_functions.j
│   ├── test_functions.s
│   ├── test_ops.j
│   └── test_ops.s
```

To run the program, call
```
./src/compile.py filename.j
```
or
```
python ./src/gen.py filename.j
```
or
```
// Compiles and execute the ./test/fib.j file
run.sh fib
```

See the [full technical report] for details of the front end, middle end and back end.

[full technical report]: ./doc/LimYanPengGary_pa3_report.pdf
