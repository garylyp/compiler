#!/usr/bin/env python

from io import TextIOWrapper
import re
import string
import sys
import time
from typing import Generator, List
from lex import Lexer

debug = False

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

    def nextToken(self):
        """
        Updates self.token with the next token from the stream
        """
        self.i += 1
        if self.i >= self.n - 1:
            print("No more tokens")
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
        return re.match(r"[a-z][A-Za-z0-9_]*", token) is not None

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
        return token == "this" or \
            token == "new" or \
            token == "(" or \
            token == "null" or \
            self.matchId(token)

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
                print(f'Expected {expected} sees {self.token} ')
                # time.sleep(1)
            currToken = self.token
            self.nextToken()
            return currToken
        else:
            self.error(expected)

    def error(self, *expected):
        print(f'Expected {list(expected)} but encountered \"{self.token}\"')
        # for i in range(len(self.stack)):
        #     print(f'{i * " "}{self.stack[i]}')
        print(self.debugOutput)
        exit(1)


    # Symbol Matching

    def parse(self):
        """
        Entry point
        """
        self.stream = self.lex()
        self.clearStream()
        self.nextToken()
        self.parseProgram()

    def parseCname(self):
        self.pushSymbol("Cname")
        if self.accept("_cname"):
            self.expect(self.token)
        else:
            self.error("cname")
        self.popSymbol()

    def parseId(self):
        self.pushSymbol("Id")
        if self.accept("_id"):
            self.expect(self.token)            
        else:
            self.error("id")
        self.popSymbol()

    def parseType(self):
        self.pushSymbol("Type")
        if self.accept("Int"):
            self.expect("Int")
        elif self.accept("Bool"):
            self.expect("Bool")
        elif self.accept("String"):
            self.expect("String")
        elif self.accept("Void"):
            self.expect("Void")
        elif self.accept("_cname"):
            self.parseCname()
        else:
            self.error("Int", "Bool", "String", "Void", "_cname")
        self.popSymbol()
        

    
    def parseProgram(self):
        self.pushSymbol("Program")
        self.parseMainClass()
        while self.token == "class":
            self.parseClassDecl()
        self.popSymbol()

    def parseMainClass(self):
        self.pushSymbol("MainClass")
        if self.accept("class"):
            self.expect("class")
            self.parseCname()
            self.expect("{")
            self.expect("Void")
            self.expect("main")
            self.expect("(")
            # Parse FmlList
            while not self.accept(")"):
                self.parseFml()
                if not self.accept(")"):
                    self.expect(",")
            self.expect(")")
            self.parseMdBody()
            self.expect("}")
        else:
            self.error("class")
        self.popSymbol()

    def parseClassDecl(self):
        self.pushSymbol("ClassDecl")
        if self.accept("class"):
            self.expect("class")
            self.parseCname()
            self.expect("{")

            # Peek to avoid unnecessary backtracking
            while self.accept("_type") and self.acceptOffset("_id", 1) and self.acceptOffset(";", 2):
                self.parseVarDecl()
            
            while not self.accept("}"):
                self.parseMdDecl()
            
            self.expect("}")
        else:
            self.error("class")
        self.popSymbol()
    
    def parseVarDecl(self):
        self.pushSymbol("VarDecl")
        self.parseType()
        self.parseId()
        self.expect(";")
        self.popSymbol()

    def parseMdDecl(self):
        self.pushSymbol("MdDecl")
        self.parseType()
        self.parseId()
        self.expect("(")
        # Parse FmlList
        while not self.accept(")"):
            self.parseFml()
            if not self.accept(")"):
                self.expect(",")
        self.expect(")")
        self.parseMdBody()
        self.popSymbol()

    def parseFml(self):
        self.pushSymbol("Fml")
        self.parseType()
        self.parseId()
        self.popSymbol()


    def parseMdBody(self):
        self.pushSymbol("MdBody")
        self.expect("{")
        while self.accept("_type") and self.acceptOffset("_id", 1) and self.acceptOffset(";", 2):
            self.parseVarDecl()
        self.parseStmt()
        while not self.accept("}"):
            self.parseStmt()
        self.expect("}")
        self.popSymbol()

    def parseStmt(self):
        self.pushSymbol("Stmt")
        if self.accept("if"):
            self.parseStmtIf()
        elif self.accept("while"):
            self.parseStmtWhile()
        elif self.accept("readln"):
            self.parseStmtReadln()
        elif self.accept("println"):
            self.parseStmtPrintln()
        elif self.accept("_id") and self.acceptOffset("=", 1):
            self.parseId()
            self.parseAssignRight()
        elif self.accept("return"):
            self.parseStmtReturn()
        elif self.accept("_atom"):
            self.parseAtom()
            if self.accept("="):
                self.parseAssignRight()
            elif self.accept(";"):
                self.expect(";")
            else:
                self.error("=", ";")
        else:
            self.error("Stmt")
        self.popSymbol()

    def parseStmtIf(self):
        self.pushSymbol("StmtIf")
        self.expect("if")
        self.expect("(")
        self.parseExp()
        self.expect(")")
        self.expect("{")
        self.parseStmt()
        while not self.accept("}"):
            self.parseStmt()
        self.expect("}")
        self.expect("else")
        self.expect("{")
        self.parseStmt()
        while not self.accept("}"):
            self.parseStmt()
        self.expect("}")
        self.popSymbol()

    def parseStmtWhile(self):
        self.pushSymbol("StmtWhile")
        self.expect("while")
        self.expect("(")
        self.parseExp()
        self.expect(")")
        self.expect("{")
        while not self.accept("}"):
            self.parseStmt()
        self.expect("}")
        self.popSymbol()

    def parseStmtReadln(self):
        self.pushSymbol("StmtReadln")
        self.expect("readln")
        self.expect("(")
        self.parseId()
        self.expect(")")
        self.expect(";")
        self.popSymbol()

    def parseStmtPrintln(self):
        self.pushSymbol("StmtPrintln")
        self.expect("println")
        self.expect("(")
        self.parseExp()
        self.expect(")")
        self.expect(";")
        self.popSymbol()

    def parseAssignRight(self):
        """
        Return root node and right child
        """
        self.pushSymbol("StmtAssign")
        self.expect("=")
        self.parseExp()
        self.expect(";")
        self.popSymbol()
    
    def parseStmtReturn(self):
        self.pushSymbol("StmtReturn")
        self.expect("return")
        if not self.accept(";"):
            self.parseExp()
        self.expect(";")
        self.popSymbol()

    def parseAtom(self):
        self.pushSymbol("Atom")
        if self.accept("this"):
            self.expect("this")
        elif self.accept("new"):
            self.expect("new")
            self.parseCname()
            self.expect("(")
            self.expect(")")
        elif self.accept("null"):
            self.expect("null")
        elif self.accept("_id"):
            self.parseId()
        elif self.accept("("):
            self.expect("(")
            self.parseExp()
            self.expect(")")
        else:
            self.error("this", "_id", "new", "(", "null")

        while self.accept(".") or self.accept("("):
            if self.accept("."):
                self.expect(".")
                self.parseId()
            elif self.accept("("):
                self.expect("(")
                while not self.accept(")"):
                    self.parseExp()
                    if self.accept(","):
                        self.expect(",")
                self.expect(")")
        self.popSymbol()

    def parseExp(self):
        self.pushSymbol("Exp")
        startIdx = int(self.i)
        
        STATE_STRING = 1 << 0
        STATE_MATH = 1 << 1
        STATE_BOOL = 1 << 2
        state = (STATE_STRING + STATE_MATH + STATE_BOOL)
        
        if self.accept("_string") or self.accept("_atom"):
            if self.accept("_string"):
                self.expect("_string")
                state &= STATE_STRING 

            elif self.accept("_atom"):
                self.parseAtom()

            while self.accept("+"):
                self.expect("+")
                if self.accept("_string"):
                    self.expect("_string")
                    state &= STATE_STRING 

                elif self.accept("_atom"):
                    self.parseAtom()

                # StringExp AND purely add on atoms MathExp guaranteed to terminate here
                
                elif self.accept("_factor"):
                    print("Backtrack to MathExp")
                    self.setToken(startIdx)
                    state &= (STATE_MATH + STATE_BOOL) 
                    break

                elif self.accept("_bool"):
                    print("Backtrack to BoolExp")
                    self.setToken(startIdx)
                    state &= STATE_BOOL
                    break
            
            if self.accept("_mathOp"):
                print("Backtrack to MathExp")
                self.setToken(startIdx)
                state &= (STATE_MATH + STATE_BOOL) 
            
            elif self.accept("_binaryOp") or self.accept("_boolOp"):
                print("Backtrack to BoolExp")
                self.setToken(startIdx)
                state = STATE_BOOL

            elif self.accept("_followExp"):
                state &= (STATE_STRING + STATE_MATH)

        elif self.accept("_factor"):
            state &= (STATE_MATH + STATE_BOOL) 

        elif self.accept("_bool"):
            state &= STATE_BOOL 

        if state == (STATE_MATH + STATE_BOOL):
            self.parseMathExp()
            if self.accept("_binaryOp"):
                print("Backtrack to BoolExp")
                self.setToken(startIdx)
                state = STATE_BOOL
            elif self.accept("_followExp"):
                state = STATE_MATH
            else:
                self.error("_binaryOp", "_followExp")
        
        if state == STATE_BOOL:
            self.parseBoolExp()
        
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

    def parseMathExp(self):
        """
        MathExp === AExp 
        """
        self.pushSymbol("MathExp")
        self.parseTerm()
        while self.accept("+") or self.accept("-"): 
            if self.accept("+"):
                self.expect("+")
            elif self.accept("-"):
                self.expect("-")
            self.parseTerm()
        self.popSymbol()
    
    def parseTerm(self):
        self.pushSymbol("Term")
        self.parseFactor()
        while self.accept("*") or self.accept("/"): 
            if self.accept("*"):
                self.expect("*")
            elif self.accept("/"):
                self.expect("/")
            self.parseFactor()
        self.popSymbol()
        
    def parseFactor(self):
        self.pushSymbol("Factor")
        while self.accept("-"): 
            # Negation
            self.expect("-")
        if self.accept("_integer"):
            self.expect("_integer")
        elif self.accept("_atom"):
            self.parseAtom()
        else:
            self.error("_integer", "_atom")
        self.popSymbol()

    def parseBoolExp(self):
        """
        BoolExp === BExp
        """
        self.pushSymbol("BoolExp")
        self.parseConj()
        while self.accept("||"):
            self.expect("||")
            self.parseConj()
        self.popSymbol()

    def parseConj(self):
        self.pushSymbol("Conj")
        self.parseRelExp()
        while self.accept("&&"):
            self.expect("&&")
            self.parseRelExp()
        self.popSymbol()

    def parseRelExp(self):
        """
        RelExp === RExp
        """
        self.pushSymbol("RelExp")
        canMathExp = True

        # BGrd
        while self.accept("!"):
            self.expect("!")
            canMathExp = False

        if self.accept("true"):
            self.expect("true")
        elif self.accept("false"):
            self.expect("false")
        elif self.accept("_atom") and not canMathExp:
            self.parseAtom()
        elif self.accept("_atom"):
            startIdx = int(self.i)
            self.parseAtom()
            
            if self.accept("_mathOp") or self.accept("_binaryOp"):
                self.setToken(startIdx)

        if (self.accept("_factor") or self.accept("_atom")) and canMathExp:
            self.parseMathExp()
            self.expect("_binaryOp")
            self.parseMathExp()

        self.popSymbol()




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
        debug = "d" in sys.argv[2]

    p = Parser(f)
    p.parse()


    f.close()