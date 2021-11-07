#!/usr/bin/env python

from io import TextIOWrapper
import re
import string
import sys
from typing import Generator, List
from lex import Lexer

debug = 0

class PNode:
    """
    Represents a node in the parse tree
    """
    def __init__(self, value):
        self.value = value
        self.children = []

    def addChild(self, item):
        self.children.append(item)

    def clear(self):
        """
        Remove all children
        """
        self.children = []


class Parser:

    def __init__(self, f: TextIOWrapper):
        """
        Parameters:
            f (TextIOWrapper): the file input stream
            stream (GeneratorObject): the token stream
            eof (boolean): describes whether end of token stream is reached
            token (string): the current token
        """
        self.f = f
        self.stream = None
        self.token = None
        self.tokens = []
        self.i = 0
        self.stack = []
        self.debugOutput = ""

    # Utility functions

    def lex(self) -> Generator:
        """
        Lex the file input 
        """
        lexer = Lexer()
        return lexer.scan(self.f)

    def clearStream(self):
        while True:
            try:
                self.tokens.append(next(self.stream))
            except StopIteration:
                break
        if debug:
            print(self.tokens)
        self.n = len(self.tokens)
        self.i = -1

    def printTree(self):
        """
        Prints the parse tree
        """
        if self.root is None:
            print("No tree constructed")
            return

        # DFS
        stk = [[self.root, 0]]
        while stk:
            node, ht = stk.pop()
            children = ""
            for c in node.children[::-1]:
                if isinstance(c, PNode):
                    children = f'[{c.value}] ' + children
                    stk.append([c, ht+1])
                else:
                    children = f'{c} ' + children
            print(f'{ht * " "}[{node.value}]: {children}')

    def nextToken(self):
        """
        Updates self.token with the next token from the stream
        """
        self.i += 1
        if self.i > self.n - 1:
            if debug: print("No more tokens")
            return
        self.token = self.tokens[self.i]

    def setToken(self, idx):
        """
        Sets self.token to the target idx. Used for backtracking
        """
        self.i = idx
        self.token = self.tokens[self.i]

    def pushSymbol(self, symbol):
        self.debugOutput += f'{len(self.stack) * " "}{symbol}\n' 
        self.stack.append(symbol)

    def popSymbol(self):
        self.stack.pop()


    # Terminal Matching

    def matchCname(sekf, token):
        return re.match(r"[A-Z][A-Za-z0-9_]*", token) is not None

    def matchId(self, token):
        return token not in ["this", "new", "null","true","false"] and \
            re.match(r"[a-z][A-Za-z0-9_]*", token) is not None

    def matchInteger(self, token):
        return re.match(r"[0-9]+", token) is not None

    def matchString(self, token):
        return re.match(r"\".*\"", token) is not None

    def matchType(self, token):
        return token == "Int" or \
            token == "Bool" or \
            token == "String" or \
            token == "Void" or \
            self.matchCname(token)

    def matchAtom(self, token):
        return token != "true" and \
            token != "false" and \
            (token == "this" or \
            token == "new" or \
            token == "(" or \
            token == "null" or \
            self.matchId(token))

    def matchFactor(self, token):
        return self.matchInteger(token) or \
            self.matchAtom(token) or \
            token == "-"

    def matchBool(self, token):
        return token == "!" or \
            token == "true" or \
            token == "false" or \
            self.matchAtom(token) or \
            self.matchFactor(token)

    def matchBinaryOp(self, token):
        return token in ["<", ">", "<=", ">=", "==", "!="]

    def matchBoolOp(self, token):
        return token in ["||", "&&"]

    def matchMathOp(self, token):
        return token in ["+", "-", "*", "/"]

    def matchFollowExp(self, token):
        return token in [")", ";", ","]

    def accept(self, expected) -> bool: 
        """
        Checks whether the current token can be accepted.
        If not accepted, will try alternative path
        """
        return self.acceptOffset(expected, 0)

    def acceptOffset(self, expected, offset) -> bool: 
        if self.i + offset >= self.n:
            return False
        token = self.tokens[self.i + offset]
        if expected == "_cname":
            return self.matchCname(token)
        elif expected == "_id":
            return self.matchId(token)
        elif expected == "_type":
            return self.matchType(token)
        elif expected == "_atom":
            return self.matchAtom(token)
        elif expected == "_integer":
            return self.matchInteger(token)
        elif expected == "_string":
            return self.matchString(token)
        elif expected == "_factor":
            return self.matchFactor(token)
        elif expected == "_bool":
            return self.matchBool(token)
        elif expected == "_boolOp":
            return self.matchBoolOp(token)
        elif expected == "_binaryOp":
            return self.matchBinaryOp(token)
        elif expected == "_mathOp":
            return self.matchMathOp(token)
        elif expected == "_followExp":
            return self.matchFollowExp(token)            
        return token == expected

    def expect(self, expected: string):
        """
        Strict. Consumes the current token if it can be accepted, else return error.
        """
        if self.accept(expected):
            if debug:
                print(f'Expected {expected} sees {self.token}')
                # time.sleep(1)
            currToken = self.token
            self.nextToken()
            return currToken
        else:
            self.error(expected)

    def error(self, *expected):
        if debug > 1:
            # print(self.debugOutput)
            self.printTree()
        # TODO: Print line number too (get from lexer)
        print(f'Parse Error: Expected {list(expected)} but encountered \"{self.token}\"')
        exit(1)


    # Symbol Matching

    def parse(self):
        """
        Entry point
        """
        self.stream = self.lex()
        self.clearStream()
        self.nextToken()
        node = self.parseProgram()
        return node

    def parseCname(self):
        self.pushSymbol("Cname")
        node = PNode(self.stack[-1])
        if self.accept("_cname"):
            node.addChild(self.expect(self.token))
        else:
            self.error("cname")
        self.popSymbol()
        return node

    def parseId(self):
        self.pushSymbol("Id")
        node = PNode(self.stack[-1])
        if self.accept("_id"):
            node.addChild(self.expect(self.token))
        else:
            self.error("id")
        self.popSymbol()
        return node

    def parseType(self):
        self.pushSymbol("Type")
        node = PNode(self.stack[-1])
        if self.accept("Int"):
            node.addChild(self.expect("Int"))
        elif self.accept("Bool"):
            node.addChild(self.expect("Bool"))
        elif self.accept("String"):
            node.addChild(self.expect("String"))
        elif self.accept("Void"):
            node.addChild(self.expect("Void"))
        elif self.accept("_cname"):
            node.addChild(self.parseCname())
        else:
            self.error("Int", "Bool", "String", "Void", "_cname")
        self.popSymbol()
        return node
        

    
    def parseProgram(self):
        self.pushSymbol("Program")
        node = PNode(self.stack[-1])
        self.root = node
        node.addChild(self.parseMainClass())
        while self.token == "class":
            node.addChild(self.parseClassDecl())
        self.popSymbol()
        return node

    def parseMainClass(self):
        self.pushSymbol("MainClass")
        node = PNode(self.stack[-1])
        if self.accept("class"):
            node.addChild(self.expect("class"))
            node.addChild(self.parseCname())
            node.addChild(self.expect("{"))
            node.addChild(self.expect("Void"))
            node.addChild(self.expect("main"))
            node.addChild(self.expect("("))
            # Parse FmlList
            while not self.accept(")"):
                node.addChild(self.parseFml())
                if not self.accept(")"):
                    node.addChild(self.expect(","))
            node.addChild(self.expect(")"))
            node.addChild(self.parseMdBody())
            node.addChild(self.expect("}"))
        else:
            self.error("class")
        self.popSymbol()
        return node

    def parseClassDecl(self):
        self.pushSymbol("ClassDecl")
        node = PNode(self.stack[-1])
        if self.accept("class"):
            node.addChild(self.expect("class"))
            node.addChild(self.parseCname())
            node.addChild(self.expect("{"))

            # Peek to avoid unnecessary backtracking
            while self.accept("_type") and self.acceptOffset("_id", 1) and self.acceptOffset(";", 2):
                node.addChild(self.parseVarDecl())
            
            while not self.accept("}"):
                node.addChild(self.parseMdDecl())
            
            node.addChild(self.expect("}"))
        else:
            self.error("class")
        self.popSymbol()
        return node
    
    def parseVarDecl(self):
        self.pushSymbol("VarDecl")
        node = PNode(self.stack[-1])
        node.addChild(self.parseType())
        node.addChild(self.parseId())
        node.addChild(self.expect(";"))
        self.popSymbol()
        return node

    def parseMdDecl(self):
        self.pushSymbol("MdDecl")
        node = PNode(self.stack[-1])
        node.addChild(self.parseType())
        node.addChild(self.parseId())
        node.addChild(self.expect("("))
        # Parse FmlList
        while not self.accept(")"):
            node.addChild(self.parseFml())
            if not self.accept(")"):
                node.addChild(self.expect(","))
        node.addChild(self.expect(")"))
        node.addChild(self.parseMdBody())
        self.popSymbol()
        return node

    def parseFml(self):
        self.pushSymbol("Fml")
        node = PNode(self.stack[-1])
        node.addChild(self.parseType())
        node.addChild(self.parseId())
        self.popSymbol()
        return node


    def parseMdBody(self):
        self.pushSymbol("MdBody")
        node = PNode(self.stack[-1])
        node.addChild(self.expect("{"))
        while self.accept("_type") and self.acceptOffset("_id", 1) and self.acceptOffset(";", 2):
            node.addChild(self.parseVarDecl())
        node.addChild(self.parseStmt())
        while not self.accept("}"):
            node.addChild(self.parseStmt())
        node.addChild(self.expect("}"))
        self.popSymbol()
        return node

    def parseStmt(self):
        self.pushSymbol("Stmt")
        node = PNode(self.stack[-1])
        if self.accept("if"):
            node.addChild(self.parseStmtIf())
        elif self.accept("while"):
            node.addChild(self.parseStmtWhile())
        elif self.accept("readln"):
            node.addChild(self.parseStmtReadln())
        elif self.accept("println"):
            node.addChild(self.parseStmtPrintln())
        elif self.accept("_id") and self.acceptOffset("=", 1): 
            leftNode = self.parseId()
            assignNode = self.parseAssignRight()
            assignNode.children.insert(0, leftNode)
            node.addChild(assignNode)
        elif self.accept("return"):
            node.addChild(self.parseStmtReturn())
        elif self.accept("_atom"):
            atomNode = self.parseAtom()
            tail = atomNode.children                

            if self.accept("="):
                if len(tail) < 3 or tail[-2] != "." or not isinstance(tail[-1], PNode) or tail[-1].value != "Id":
                    # ... "." Id
                    self.error("_atom . _id")
                assignNode = self.parseAssignRight()
                assignNode.children.insert(0, atomNode)
                node.addChild(assignNode)
            elif self.accept(";"):
                # atom cannot be just
                # this, null, id, (Exp,Exp), new cname ()
                if len(tail) < 3 or \
                    tail[-3] != "(" or \
                    not isinstance(tail[-2], PNode) or tail[-2].value != "ExpList" or \
                    tail[-1] != ")":
                    self.error("_atom ( ExpList )")
                node.addChild(atomNode)
                node.addChild(self.expect(";"))
            else:
                self.error("=", ";")
        else:
            self.error("Stmt")
        self.popSymbol()
        return node

    def parseStmtIf(self):
        self.pushSymbol("StmtIf")
        node = PNode(self.stack[-1])
        node.addChild(self.expect("if"))
        node.addChild(self.expect("("))
        node.addChild(self.parseExp())
        node.addChild(self.expect(")"))
        node.addChild(self.expect("{"))
        node.addChild(self.parseStmt())
        while not self.accept("}"):
            node.addChild(self.parseStmt())
        node.addChild(self.expect("}"))
        node.addChild(self.expect("else"))
        node.addChild(self.expect("{"))
        node.addChild(self.parseStmt())
        while not self.accept("}"):
            node.addChild(self.parseStmt())
        node.addChild(self.expect("}"))
        self.popSymbol()
        return node

    def parseStmtWhile(self):
        self.pushSymbol("StmtWhile")
        node = PNode(self.stack[-1])
        node.addChild(self.expect("while"))
        node.addChild(self.expect("("))
        node.addChild(self.parseExp())
        node.addChild(self.expect(")"))
        node.addChild(self.expect("{"))
        while not self.accept("}"):
            node.addChild(self.parseStmt())
        node.addChild(self.expect("}"))
        self.popSymbol()
        return node

    def parseStmtReadln(self):
        self.pushSymbol("StmtReadln")
        node = PNode(self.stack[-1])
        node.addChild(self.expect("readln"))
        node.addChild(self.expect("("))
        node.addChild(self.parseId())
        node.addChild(self.expect(")"))
        node.addChild(self.expect(";"))
        self.popSymbol()
        return node

    def parseStmtPrintln(self):
        self.pushSymbol("StmtPrintln")
        node = PNode(self.stack[-1])
        node.addChild(self.expect("println"))
        node.addChild(self.expect("("))
        node.addChild(self.parseExp())
        node.addChild(self.expect(")"))
        node.addChild(self.expect(";"))
        self.popSymbol()
        return node

    def parseAssignRight(self):
        """
        Return root node and right child
        """
        self.pushSymbol("StmtAssign")
        node = PNode(self.stack[-1])
        node.addChild(self.expect("="))
        node.addChild(self.parseExp())
        node.addChild(self.expect(";"))
        self.popSymbol()
        return node
    
    def parseStmtReturn(self):
        self.pushSymbol("StmtReturn")
        node = PNode(self.stack[-1])
        node.addChild(self.expect("return"))
        if not self.accept(";"):
            node.addChild(self.parseExp())
        node.addChild(self.expect(";"))
        self.popSymbol()
        return node

    def parseAtom(self):
        self.pushSymbol("Atom")
        node = PNode(self.stack[-1])
        if self.accept("this"):
            node.addChild(self.expect("this"))
        elif self.accept("new"):
            node.addChild(self.expect("new"))
            node.addChild(self.parseCname())
            node.addChild(self.expect("("))
            node.addChild(self.expect(")"))
        elif self.accept("null"):
            node.addChild(self.expect("null"))
        elif self.accept("_id"):
            node.addChild(self.parseId())
        elif self.accept("("):
            node.addChild(self.expect("("))
            node.addChild(self.parseExp())
            node.addChild(self.expect(")"))
        else:
            self.error("this", "_id", "new", "(", "null")

        while self.accept(".") or self.accept("("):
            if self.accept("."):
                node.addChild(self.expect("."))
                node.addChild(self.parseId())
            elif self.accept("("):
                node.addChild(self.expect("("))
                # Special case, only ExpList handled like this 
                # because we need to verify pattern for stmts
                node.addChild(self.parseExpList())
                node.addChild(self.expect(")"))
        self.popSymbol()
        return node

    def parseExpList(self):
        self.pushSymbol("ExpList")
        node = PNode(self.stack[-1])
        while not self.accept(")"): # FOLLOW(ExpList)
            node.addChild(self.parseExp())
            if self.accept(","):
                node.addChild(self.expect(","))
        self.popSymbol()
        return node

    def parseExp(self):
        self.pushSymbol("Exp")
        node = PNode(self.stack[-1])
        startIdx = int(self.i)
        
        STATE_STRING = 1 << 0
        STATE_MATH = 1 << 1
        STATE_BOOL = 1 << 2
        state = (STATE_STRING + STATE_MATH + STATE_BOOL)
        
        if self.accept("_string") or self.accept("_atom"):
            if self.accept("_string"):
                node.addChild(self.expect("_string"))
                state &= STATE_STRING 

            elif self.accept("_atom"):
                node.addChild(self.parseAtom())

            while self.accept("+"):
                node.addChild(self.expect("+"))
                if self.accept("_string"):
                    node.addChild(self.expect("_string"))
                    state &= STATE_STRING 

                elif self.accept("_atom"):
                    node.addChild(self.parseAtom())

                # StringExp AND purely add on atoms MathExp guaranteed to terminate here
                
                elif self.accept("_factor"):
                    if debug: print("Backtrack to MathExp")
                    self.setToken(startIdx)
                    node.clear()
                    state &= (STATE_MATH + STATE_BOOL) 
                    break

                elif self.accept("_bool"):
                    if debug: print("Backtrack to BoolExp")
                    self.setToken(startIdx)
                    node.clear()
                    state &= STATE_BOOL
                    break
            
            if self.accept("_mathOp"):
                if debug: print("Backtrack to MathExp")
                self.setToken(startIdx)
                node.clear()
                state &= (STATE_MATH + STATE_BOOL) 
            
            elif self.accept("_binaryOp") or self.accept("_boolOp"):
                if debug: print("Backtrack to BoolExp")
                self.setToken(startIdx)
                node.clear()
                state = STATE_BOOL

            elif self.accept("_followExp"):
                state &= (STATE_STRING + STATE_MATH)

        elif self.accept("_factor"):
            state &= (STATE_MATH + STATE_BOOL) 

        elif self.accept("_bool"):
            state &= STATE_BOOL 

        if state == (STATE_MATH + STATE_BOOL):
            node.addChild(self.parseMathExp())
            if self.accept("_binaryOp"):
                if debug: print("Backtrack to BoolExp")
                self.setToken(startIdx)
                node.clear()
                state = STATE_BOOL
            elif self.accept("_followExp"):
                state = STATE_MATH
            else:
                self.error("_binaryOp", "_followExp")
        
        if state == STATE_BOOL:
            node.addChild(self.parseBoolExp())
        
        if state == (STATE_STRING + STATE_MATH + STATE_BOOL):
            # Probably just an atom
            pass

        if state == (STATE_STRING + STATE_MATH):
            # Probably sum of atoms
            pass
            
        if not self.accept("_followExp"):
            self.error("_followExp")

        # at the end, you must assign a type to  the expression
        self.popSymbol()
        return node

    def parseMathExp(self):
        """
        MathExp === AExp 
        """
        self.pushSymbol("MathExp")
        node = PNode(self.stack[-1])
        node.addChild(self.parseTerm())
        while self.accept("+") or self.accept("-"): 
            if self.accept("+"):
                node.addChild(self.expect("+"))
            elif self.accept("-"):
                node.addChild(self.expect("-"))
            node.addChild(self.parseTerm())
        self.popSymbol()
        return node
    
    def parseTerm(self):
        self.pushSymbol("Term")
        node = PNode(self.stack[-1])
        node.addChild(self.parseFactor())
        while self.accept("*") or self.accept("/"): 
            if self.accept("*"):
                node.addChild(self.expect("*"))
            elif self.accept("/"):
                node.addChild(self.expect("/"))
            node.addChild(self.parseFactor())
        self.popSymbol()
        return node
        
    def parseFactor(self):
        self.pushSymbol("Factor")
        node = PNode(self.stack[-1])
        while self.accept("-"): 
            # Negation
            node.addChild(self.expect("-"))
        if self.accept("_integer"):
            node.addChild(self.expect("_integer"))
        elif self.accept("_atom"):
            node.addChild(self.parseAtom())
        else:
            self.error("_integer", "_atom")
        self.popSymbol()
        return node

    def parseBoolExp(self):
        """
        BoolExp === BExp
        """
        self.pushSymbol("BoolExp")
        node = PNode(self.stack[-1])
        node.addChild(self.parseConj())
        while self.accept("||"):
            node.addChild(self.expect("||"))
            node.addChild(self.parseConj())
        self.popSymbol()
        return node

    def parseConj(self):
        self.pushSymbol("Conj")
        node = PNode(self.stack[-1])
        node.addChild(self.parseRelExp())
        while self.accept("&&"):
            node.addChild(self.expect("&&"))
            node.addChild(self.parseRelExp())
        self.popSymbol()
        return node

    def parseRelExp(self):
        """
        RelExp === RExp
        """
        self.pushSymbol("RelExp")
        node = PNode(self.stack[-1])
        canMathExp = True

        # BGrd
        while self.accept("!"):
            node.addChild(self.expect("!"))
            canMathExp = False

        if self.accept("true"):
            node.addChild(self.expect("true"))
        elif self.accept("false"):
            node.addChild(self.expect("false"))
        elif self.accept("_atom") and not canMathExp:
            node.addChild(self.parseAtom())
        elif self.accept("_atom"):
            startIdx = int(self.i)
            node.addChild(self.parseAtom())
            
            if self.accept("_mathOp") or self.accept("_binaryOp"):
                if debug: print("Backtrack to MathExp")
                self.setToken(startIdx)
                node.clear()

        if (self.accept("_factor") or self.accept("_atom")) and canMathExp:
            node.addChild(self.parseMathExp())
            node.addChild(self.expect("_binaryOp"))
            node.addChild(self.parseMathExp())

        self.popSymbol()
        return node




if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Usage: python parse.py filename")
        print("Usage: ./parse.py filename")
        exit(1)

    filename = sys.argv[1]
    try:
        f = open(filename)
    except FileNotFoundError as e:
        print(e)
        exit(1)

    if len(sys.argv) > 2:
        debug = int(sys.argv[2])

    p = Parser(f)
    p.parse()
    f.close()
    
    if p.i < len(p.tokens):
        if debug: p.printTree()
        print(f'Parse Error: tokens remaining after parsing completed: {p.tokens[p.i:]}')
    else:
        p.printTree()