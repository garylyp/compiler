#!/usr/bin/env python

import sys
from lex import Lexer

class Parser:

    def __init__(self, f):
        self.f = f

    def lex(self):
        lexer = Lexer()
        lexer.scan(self.f)

    def parse():
        print("parse ")


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Usage: python parser.py filename")
        exit(1)

    filename = sys.argv[1]
    try:
        f = open(filename)
    except FileNotFoundError as e:
        print(e)
        exit(1)

    p = Parser(f)
    p.lex()


    f.close()