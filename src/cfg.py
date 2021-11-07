from ir3 import *

class Block:
    """
    Represents a basic block in a control flow. Can contain multiple statements
    """
    name:str
    stmts:'list[Stmt]' 
    parents:'list[Block]'
    children:'list[Block]'
    inVars:'list[str]'
    outVars:'list[str]'

    def __init__(self, name:str) -> None:
        self.name = name
        self.stmts = []
        self.parents = []
        self.children = []

    def addStmt(self, stmt:'Stmt'):
        self.stmts.append(stmt)

    def addParent(self, block:'Block'):
        self.parents.append(block)

    def addChildren(self, block:'Block'):
        self.children.append(block)

    def pprint(self) -> str:
        res = f'{self.name} {[p.name for p in self.parents]} {[c.name for c in self.children]}' + "\n"
        for s in self.stmts:
            res += s.pprint() 
            res += "\n"
        return res
        

class CFG:
    """
    Constructs a CFG for a list of stmts (from CMtd) 
    """
    root:'Block'
    leaf:'Block'
    blockNum:'int'
    blockMap:'dict[str,Block]'
    stmts:'list[Stmt]'

    def __init__(self, stmts:'list[Stmt]') -> None:
        self.stmts = stmts
        self.blockNum = 0
        self.blockMap = {}

    def newName(self) -> str:
        """
        returns the next block name based on the block number
        """
        num = f'B{self.blockNum}'
        self.blockNum += 1
        return num

    def build(self) -> 'Block':
        name = self.newName()
        curr = Block(name)
        self.blockMap[name] = curr
        self.root = curr
        self.base = curr

        i = 0
        n = len(self.stmts)
        # Link consecutive blocks (without goto)
        while i < n:
            if isinstance(self.stmts[i], LabelStmt):
                newName = f'L{self.stmts[i].labelNum}'
                next = Block(newName)
                self.blockMap[newName] = next
                next.addStmt(self.stmts[i])

                # curr is not an empty block
                if curr is not None:
                    next.addParent(curr)
                    curr.addChildren(next)    
                curr = next
                self.base = curr

            elif isinstance(self.stmts[i], IfStmt):
                curr.addStmt(self.stmts[i])
                newName = self.newName()
                next = Block(newName)
                next.addParent(curr)
                self.blockMap[newName] = next
                curr.addChildren(next)
                curr = next
                self.base = curr

            elif isinstance(self.stmts[i], GotoStmt):
                curr.addStmt(self.stmts[i])
                self.base = curr
                curr = None

            else:
                curr.addStmt(self.stmts[i]),
            
            i+=1

        # Link blocks by goto
        for blockName in self.blockMap:
            block = self.blockMap[blockName]
            if not block.stmts:
                print(f'Build CFG Error: empty block {blockName}')
                continue
                
            lastStmt = block.stmts[-1]
            if isinstance(lastStmt, GotoStmt) or isinstance(lastStmt, IfStmt):
                jumpName = f'L{lastStmt.labelNum}'
                jumpBlock = self.blockMap[jumpName]
                block.addChildren(jumpBlock)
                jumpBlock.addParent(block)

        return self.root

    def getRoot(self):
        return self.root

    def pprint(self):
        res = ""
        for blockName in self.blockMap:
            res += self.blockMap[blockName].pprint()
            res += "\n"

        print(f'root: {self.root.name}')
        print(f'base: {self.base.name}')
        return res
    
