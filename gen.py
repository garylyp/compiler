#!/usr/bin/env python

import sys
from io import TextIOWrapper

from parse import Parser
from ast2 import *
from ir3 import Generator

class Gen:
    def genIR3(self, f: TextIOWrapper) -> str:
        p = Parser(f)
        parseTree = p.parse()
        f.close()

        ast = AST(parseTree)
        c = Checker()
        c.loadAST(ast)
        c.checkNames()
        c.checkTypes()

        g = Generator(ast)
        g.genProgram()
        g.trimLabels()
        g.backpatch()
        g.printIR3()

        self.ir3 = g.program.pprint()

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Usage: python gen.py filename")
        print("Usage: ./gen.py filename")
        exit(1)

    filename = sys.argv[1]
    try:
        f = open(filename)
    except FileNotFoundError as e:
        print(e)
        exit(1)

    gen = Gen()
    gen.genIR3(f)
