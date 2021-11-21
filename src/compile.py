#!/usr/bin/env python

import sys, os

from parse import Parser, PNode
from ast2 import *
from ir3 import Generator, Program
from arm import ArmGenerator

class Compiler:
    def compile(self, filename:str):

        # FRONT END: Lexing and Parsing
        parseTree = self.parse(filename)
        ast = AST(parseTree)

        # MIDDLE END: Type checker and intermediate code generator
        self.check(ast)
        program = self.genIR3(ast)

        # BACK END: Arm code generator
        self.genARM(program)
        
    
    def parse(self, filename:str) -> PNode:
        with open(filename) as f:
            p = Parser(f)
            parseTree = p.parse()
        return parseTree

    def check(self, ast:AST): 
        c = Checker()
        c.loadAST(ast)
        c.checkNames()
        c.checkTypes()

    def genIR3(self, ast:AST) -> Program:
        g = Generator(ast)
        program = g.gen()
        return program

    def genARM(self, program:'Program') -> str:
        a = ArmGenerator(program)
        a.genArm()


def readFile():
    if (len(sys.argv) < 2):
        print("Usage: python compile.py filename.j")
        print("Usage: ./compile.py filename.j")
        exit(1)
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print(f'File \'{filename}\' not found')
        exit(1)
    return filename


if __name__ == '__main__':
    filename = readFile()
    c = Compiler()
    c.compile(filename)