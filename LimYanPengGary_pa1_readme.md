# compiler
A recursive descent compiler capable of parsing JLite into ARM assembly code

# Lexer
The lexer is desgined like a finite state machine. The default state is START. Depending on what characters are seen next, the state changes and characters are consumed to form tokens. This continues until a specific end character is encountered, whereby the state goes back to START again.

List of states:
* `STATE_START` - default
* `STATE_NAME` - when [A-Za-z] is encountered at start
* `STATE_DIGIT` - when [0-9] is encountered at start
* `STATE_COMP` - when ><=! is encountered at start
* `STATE_BAR` - when | is encountered at start
* `STATE_AND` - when & is encountered at start
* `STATE_STRING` - when " is encountered at start
* `STATE_SINGLE_SLASH` - when / is encountered at start

Each of these states may transit to other states depending on what characters are being consumed.

The output is a list of strings of all recognizable terminal symbols with the comments stripped away. The terminal symbols, also referred to as tokens, will be passed to the parser to be processed one by one.

# Parser
## Overview
The parser accomplishes its tasks by advancing tokens one by one (and occasionally performing lookaheads) to match symbols described in the JLite grammar. It starts off by parsing the `Program`, within which it will attempt to parse the `MainClass`, `ClassDecl` and so on. 

## Instruments
The parser contains 3 main types of functions:
* `accept` - checks whether the next token can be accepted. Used for solving ambiguities
* `expect` - Ensures a token (terminal) can be accepted, then consumes it and advances to the next token
* `parse` - Similar to `expect`, but for symbols

## Symbols
The logic for parsing any symbol `XXX` is contained within the function `parseXXX`. This function will `expect` terminals or `parse` symbols in a specific order according to JLite specifications. For example, parsing the symbol `VarDecl` would happen in 3 steps:
1. parse `Type`
2. parse `Id`
3. expect `;`

## Terminals
For each symbol, if it expects to see a terminal (i.e. this particular terminal must occur at this position), it will check that the current token is indeed the terminal (`accept`) before consuming it. The above logic is executed within the`expect` function.

## Ambiguities
There are a few cases of ambiguities in the JLite grammar. This is first addressed by doing left-factoring or removal of left-recursion in the grammar whenever possible. But this will not solve all ambiguities. The following highlights some strategies that are used in the parser:

1. Lookahead
```
<ClassDecl> --> class <cname> { <VarDecl>*  <MdDecl>+ }
<VarDecl>   --> <Type> <Id> ;
<MdDecl>    --> <Type> <Id> ( <FmlList> ) <MdBody>
...
```
In the above example, when parsing ClassDecl, we do not know where is the end of the `VarDecl` list since it shares the same prefix as `MdDecl`. However, a notable difference between `VarDecl` and `MdDecl` is that `VarDecl` expects a `;` in the 3rd position. We can thus lookahead by 2 symbols to see whether it is the end of the `VarDecl` list.

2. Backtracking

In the resolving of expressions, it is difficult to determine from the first symbol what the expression type could be, especially if the first symbol is an atom, since all three expresion types could begin with atom.

```
// String
atom1 + atom2 + atom3 + STRING_LITERAL

// Arithmetic
atom1 + atom2 + atom3 + 2

// Boolean
atom1 + atom2 + atom3 + 2 >= 0
```
In case 1, we can only confirm that it is a String Exp only after we see the STRING_LITERAL. 

In case 2, we might wrongly assume that it is a String expression until we see the first INTEGER_LITERAL. In that case, we have to backtrack and reparse the atoms as a Arithmetic Expression.

In case 3, we might wrongly assume that the whole expression is an Arithmetic Expression until we see the binary operator. In that case, we have to backtrack and reparse the atoms as a Boolean Expression.

