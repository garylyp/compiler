#!/usr/bin/env python

from ir3 import Program, CMtd, CData
from cfg import CFG, Block

class ArmGenerator:
    def __init__(self, program:'Program') -> None:
        self.program = program

    def buildObjectDescriptor(self, cdata:'CData'):
        pass

    def buildCFG(self, cMtd:'CMtd'):
        stmts = cMtd.mdBody.stmts
        b = CFG(stmts)
        root = b.build()
        print(b.pprint())


