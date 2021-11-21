# Static Checker

The Static Checker consists of two steps. Name Checking and Type Checking.

## Directory Structure

```
├── LimYanPengGary_pa2_readme.md
├── lex.py   // Lexer
├── parse.py // Parser - generates Parse Tree from tokens
├── ast2.py  // Generates AST from Parse Tree and performs Static Checking
├── gen.py   // Main entry point of the code 
├── ir3.py   // Generates IR3 from AST
├── run.bat  // Script to run all test files
└── test     // List of test files
    ├── parse  // List of old test files
    ...
```

To run the program, call
```
./gen.py filename.j
```
or
```
python gen.py filename.j
```

## Name Checking

1. Convert parse tree to AST 

The output of the parser actually generates a parse tree that contains a lot of unnecessary symbols like `;`. The parse tree thus has to be converted into a proper AST. This step was surprisingly laborious, especially since the children of each parse tree nodes are composed of mixtures of other nodes and strings, which means theres a lot of code logic required to verify the type of the children. The step here could have been avoided had I constructed the AST directly from part 1 of the assignment instead of the intermediate parse tree that had aided me in the pretty printing.

2. Name Checking

First, I check for existence of duplicate class names by storing each class name as a key in a dictionary. 

After which, I adopted the same method for checking the existence of duplicate class fields and method variables. Basically, each field / variable name and its type is stored as a key-value pair in a dictionary.

The checking of duplicate method declaration is slightly more complex as my compiler allows **method overloading**. To go about distinguishing methods with the same name but different sequence of parameter types, a two level dictionary was used. The set of all possible methods for a class is stored in a dictionary that maps method names to another dictionary, where the inner dictionary maps a tuple of strings (representing the method's parameter types) to the return type of the method. This allows methods of the same name but different sequence of argument types (e.g. a(Int x, Bool y) and a(Int x, String y)) to be distinguished by the inner dictionary.

## Type Checking

This part is implemented based on Assignment specifications. A `TypeEnvironment` object is prepared before the start of the type checking for each **method**. This object maps classnames to the dictionary of methods and the set of fields (and their types). The local variables (actual and formal variables) of a method is also stored within the `TypeEnvironment`. This allows method types, return types and expression types to be easily verified when traversing down the AST.

Most expressions and statements have an expected type associated with it. For example, the type of an `add` expression can either be a `String` or an `Int` expression. To further resolve this, it will inherit the type of the left expression. The right expression will subsequently need to match the type of the `add` expression. The type of a `Call` statement will depend on the return type of the method being called. Some other checks include:
- type of expressions of `return` statements match the return type of the method
- last statements of each method match the return type of the method
- last statements of then and else block of `if` statements match each other

For `call` statements, the calling class must be resolved first. It can either be the `this` class for a local call or a class represented by some expressions. Subsequently, the types of each argument expression are also resolved. Only then can we check that the class, contains a method with the respective parameters.

For field access or variable access, the concept is similar to calls. For variables, if it does not belong in the scope of the method, it will check the type environment to look for the variable id from the fields of the current class. Field access are directly checked against the type environment to verify if the class has a field with the particular id.

`Null` literals will take on the expected type of the expression it is used in. If it is used as a `return` expression, `Null` will take on the return type of the method where the `return` statement is found, provided that the type is `Nullable` (includes all defined classes and String).

# Intermediate Code Generator
In the AST, every statement node will be resolved into a sequence of IR3 statements that will be concatenated together based on the order of the AST statement in the block. Every expression node will be resolved into a sequence of IR3 statements as well as an identifier, which can be a temporarily initialized variable. Children nodes will pass on their generated IR3 to the parent nodes to be merged.

## Optimizations
Some optimization methods adopted are:
- Eliminating unreachable code
- Flow-of-control optimizations (multiple consecutive jumps)

For example unreachable statements following a `goto` statement and preceding any other `label` statements are removed. Consecutive jumps are also collapsed as follows.

e.g.
```
Label 1:
    goto 2;
Label 2:
    goto 3;
Label 3:
    goto 4;
```
becomes
```
Label 1:
    goto 4;
Label 2:
    goto 4;
Label 3:
    goto 4;
```
If Labels 2 and 3 are not used, the above is further reduced.
```
Label 1:
    goto 4;
```