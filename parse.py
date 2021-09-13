#!/usr/bin/env python

from io import TextIOWrapper
import re
import string
import sys
import time
from typing import Generator, List
from lex import Lexer

slow = False

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

    def matchCname(sekf, token):
        return re.match(r"[A-Z][A-Za-z0-9_]*", token)

    def matchId(sekf, token):
        return re.match(r"[a-z][A-Za-z0-9_]*", token)

    def matchType(self, token):
        return token == "Int" or \
            token == "Bool" or \
            token == "String" or \
            token == "Void" or \
            self.matchCname(token)

    def accept(self, expected) -> bool: 
        """
        Checks whether the current token can be accepted.
        If not accepted, will try alternative path
        """
        if expected == "_cname":
            return self.matchCname(self.token)
        elif expected == "_id":
            return self.matchId(self.token)
        elif expected == "_type":
            return self.matchType(self.token)
        return self.token == expected

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
        return token == expected

    def expect(self, expected: string):
        """
        Consumes the current token if it matches expected, else return error.
        """
        if self.accept(expected):
            if slow:
                print(f'See {self.token}, expect {expected}')
                time.sleep(1)
            currToken = self.token
            self.nextToken()
            return currToken
        else:
            self.error(expected)

    def error(self, expected):
        print(f'Expected \"{expected}\" but encountered \"{self.token}\"')
        for i in range(len(self.stack)):
            print(f'{i * " "}{self.stack[i]}')
        exit(1)

    def pushSymbol(self, symbol):
        self.stack.append(symbol)

    def popSymbol(self):
        self.stack.pop()

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
            self.error("Type")
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
            self.parseFmlList()
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

            if self.accept("}"):
                self.expect("}")
                return

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
        if not self.accept(")"):
            self.parseFmlList()
        self.expect(")")
        self.parseMdBody()
        self.popSymbol()

    def parseFmlList(self):
        self.pushSymbol("FmlList")
        self.parseFml()
        while self.accept(","):
            self.expect(",")
            self.parseFml()
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
        # self.parseStmt()
        while not self.accept("}"):
            print(self.stack)
            print(self.token)
            # self.parseStmt()
            x=1
        self.expect("}")
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
        slow = sys.argv[2] == "slow"

    p = Parser(f)
    p.parse()


    f.close()