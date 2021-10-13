# Static Checker

The Static Checker consists of two steps. Name Checking and Type Checking.

## Name Checking

1. Convert parse tree to AST 

This step was surprisingly laborious, especially since the children of each parse tree nodes are composed of mixtures of other nodes and strings, which means theres a lot of code logic required to verify the type of the children. The step here could have been avoided had I constructed the AST directly from part 1 of the assignment instead of the intermediate parse tree that had aided me in the pretty printing.

2. Check names

First, I check for existence of duplicate class names by storing each class name as a key in a dictionary. 

After which, I adopted the same method for checking the existence of duplicate class fields and method variables. Basically, each field / variable name and its type is stored as a key-value pair in a dictionary.

The checking of duplicate method declaration is slightly more complex as my compiler allows **method overloading**. To go about distinguishing methods with the same name but different sequence of parameter types, a two level dictionary approach was used. The set of all possible methods for a class is stored in a dictionary that maps method names to another dictionary, where the inner dictionary maps a tuple of strings (representing the method parameter types) to the return type of the method. This allows methods of the same name but different argument types (e.g. a(Int x, Bool y) and a(Int x, String y)) to be distinguished by the inner dictionary.

## Type Checking

This part is implemented based on Assignment specifications. Type Checking is performed from the leaf of the AST to the Root. For example, the type of an `add` expression will inherit the type of the left expression. The right expression will subsequently need to match the type of the `add` expression. The type of a `Call` statement will depend on the return type of the method being called. Some other checks include:
- type of expressions of `return` statements match the return type of the method
- last statements of each method match the return type of the method
- last statements of then and else block of `if` statements match each other


`Null` literals will take on the expected type of the expression it is used in. If it is used as a `return` expression, `Null` will take on the return type of the method where the `return` statement is found, provided that the type is `Nullable` (includes all defined classes and String).

# Intermediate Code Generator


## Optimizations
Unreachable Goto statements are removed. Redundant Labels (with only a single Goto stmt in its block) are also merged with Labels that is specified by its sole Goto stmt.

e.g.
```
Label 2:
    goto 3;
Label 3:
    goto 5;
```
becomes
```
Label 2:
    goto 5;
```