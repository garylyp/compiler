import re

from ir3 import *
from constants import *

NON_VAR_SYMBOLS = {"+", "-", "*", "/", ">", ">=", "<", "<=", "==", "!=", ".", "()", "new", "", "null"}

INT_TYPE = "Int"
INT_SIZE = 4
STR_TYPE = "String"
STR_SIZE = 4 # String pointr
BOOL_TYPE = "Bool"
BOOL_SIZE = 1
VOID_TYPE = "Void"
PTR_SIZE = 4

def isVar(s):
    return s not in NON_VAR_SYMBOLS and \
        not isStringLiteral(s) and \
        not isIntLiteral(s) and \
        not isBoolLiteral(s) and \
        not isCname(s) 

def isStringLiteral(s):
    return re.match(r"\".*\"", s) is not None

def isCname(s):
    return re.match(r"[A-Z][A-Za-z0-9_]*", s) is not None

def isIntLiteral(s):
    return re.match(r"[0-9]+", s) is not None

def isBoolLiteral(s):
    return s in ["true", "false"]

def isArithOp(s):
    return s in ["+", "-", "*", "/"]

################################################################################################

# CFG

################################################################################################

class Block:
    """
    Represents a basic block in a control flow. Can contain multiple statements
    """
    name:str
    stmts:'list[Stmt]' 
    parents:'list[Block]'
    children:'list[Block]'
    inVars:'set[str]'
    outVars:'set[str]'
    blockInfo:'BlockInfo'

    def __init__(self, name:str) -> None:
        self.name = name
        self.stmts = []
        self.parents = []
        self.children = []
        self.inVars = set()
        self.outVars = set()

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
        
def newCFG(stmts:'list[Stmt]') -> 'CFG':
    cfg = CFG(stmts)
    cfg.build()
    return cfg

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
                # print(f'Build CFG Error: empty block {blockName}')
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

class BlockInfo:
    """
    Contains crucial information of register mapping at each line
    """

    livePerLine:'list[dict[str,int]]' 
    """
    Maps each live variable to its next use
    """
    usePerLine:'list[set[str]]' 
    """
    Shows the set of variables used in the current line
    """
    defPerLine:'list[set[str]]'
    """
    Shows the set of variables defined in the current line
    """
    varToRegPerLine:'list[dict[str,str]]'
    """
    Shows the variable to register mapping at the current line
    """
    varToMemPerLine:'list[dict[str,str]]'
    """
    Shows the variable to mem location (of current stack frame, from sp) mapping at the current line
    """
    regToVarPerLine:'list[dict[str,str]]'
    """
    Shows the register to variable mapping the current line
    """
    stkToVarPerLine:'list[dict[str,str]]'
    """
    Shows the variable to mem location (of items to be placed onto the stack, from incremented sp) mapping at the current line. 
    Used before function call
    """
    def __init__(self) -> None:
        self.livePerLine = None
        self.defPerLine = None
        self.varToRegPerLine = None
        self.varToMemPerLine = None

################################################################################################

# Symbol Table

################################################################################################

class ClassStackInfo:
    cname:'str'
    size:'int'
    """
    Size of the pointer for this class (or size of this type for primitives Bool Int String)
    """
    fieldOffsetMap:'dict[str,int]'
    offset:'int'
    """
    Max offset. Also refers to the size required for this entire object
    """
    def __init__(self, cname:str, size:int) -> None:
        self.cname = cname
        self.size = size
        self.offset = 0
        self.fieldOffsetMap = {}

    def getBodySize(self) -> int:
        return self.offset

    def addField(self, fieldId, fieldSize):
        self.fieldOffsetMap[fieldId] = int(self.offset)
        self.offset += fieldSize

    def getFieldOffset(self, fieldId):
        return self.fieldOffsetMap[fieldId]

class VarStackInfo:
    id:'str'
    varType:'str'
    size:'int'
    valueInfo:'str' # to check the current value of a var during runtime
    def __init__(self, id:str, varType:str, size:int) -> None:
        self.id = id
        self.varType = varType
        self.size = size

class SymbolTable:
    classInfoMap:'dict[str,ClassStackInfo]'
    varInfoMap:'dict[str,dict[str,VarStackInfo]]'
    methodInfoMap:'dict[str,RegAllocator]'
    def __init__(self) -> None:
        self.classInfoMap = {}
        self.varInfoMap = {}
        self.methodInfoMap = {}
        self.initDefaultTypes()

    def initDefaultTypes(self):
        intInfo = ClassStackInfo(INT_TYPE, INT_SIZE)
        self.classInfoMap[INT_TYPE] = intInfo

        strInfo = ClassStackInfo(STR_TYPE, STR_SIZE)
        self.classInfoMap[STR_TYPE] = strInfo

        boolInfo = ClassStackInfo(BOOL_TYPE, BOOL_SIZE)
        self.classInfoMap[BOOL_TYPE] = boolInfo

    # Setter
    def addClassInfo(self, cname:str, classInfo:'ClassStackInfo'):
        self.classInfoMap[cname] = classInfo

    def addVarInfo(self, methodId:str, varId:str, varInfo:'VarStackInfo'):
        if methodId not in self.varInfoMap:
            self.varInfoMap[methodId] = { varId : varInfo }
        else:
            self.varInfoMap[methodId][varId] = varInfo

    def populateVarStackInfo(self, cMtd:'CMtd'):
        methodId = cMtd.id
        # Add formals
        for f in cMtd.formals:
            varType = f.type
            varId = f.id
            varSize = self.getTypeSize(varType)
            varInfo = VarStackInfo(varId, varType, varSize)
            self.addVarInfo(methodId, varId, varInfo)

        # Add actuals
        for f in cMtd.mdBody.varDecl:
            varType = f.type
            varId = f.id
            varSize = self.getTypeSize(varType)
            varInfo = VarStackInfo(varId, varType, varSize)
            self.addVarInfo(methodId, varId, varInfo)

        # Add variables defined in stmts
        for s in cMtd.mdBody.stmts:
            if not isinstance(s, AssignTypeIdStmt):
                continue
            varType = s.type
            varId = s.id
            varSize = self.getTypeSize(varType)
            varInfo = VarStackInfo(varId, varType, varSize)
            self.addVarInfo(methodId, varId, varInfo)

    def addMethodInfo(self, methodId:str, regAlloc:'RegAllocator'):
        self.methodInfoMap[methodId] = regAlloc

    # Getter
    def getFieldOffsetForClass(self, cname:str, fieldId:str):
        if cname not in self.classInfoMap:
            print(f'Symbol Table Error: class {cname} not found in symbol table')
            exit(1)
        if fieldId not in self.classInfoMap[cname].fieldOffsetMap:
            print(f'Symbol Table Error: field {cname}.{fieldId} not found in symbol table')
            exit(1)
        return self.classInfoMap[cname].fieldOffsetMap[fieldId]

    def getVarInfoFromMethod(self, methodId:str, varId:str):
        if methodId not in self.varInfoMap:
            print(f'Symbol Table Error: method {methodId} not found in symbol table')
            exit(1)
        if varId not in self.varInfoMap[methodId]:
            print(f'Symbol Table Error: var {varId} not found in symbol table for method {methodId}')
            exit(1)
        return self.varInfoMap[methodId][varId]

    def getVarTypeFromMethod(self, methodId:str, varId:str):
        varInfo = self.getVarInfoFromMethod(methodId, varId)
        return varInfo.varType

    def getTypeSize(self, typename:str) -> int:
        if typename in self.classInfoMap:
            return self.classInfoMap[typename].size
        else:
            print(f'Symbol Table Error: type {typename} not found in symbol table')
            exit(1)

    def getClassBodySize(self, cname:str) -> int:
        if cname in self.classInfoMap:
            return self.classInfoMap[cname].offset
        else:
            print(f'Symbol Table Error: type {cname} not found in symbol table')
            exit(1)

    def getMethodInfo(self, methodId:str) -> 'RegAllocator':
        if methodId in self.methodInfoMap:
            return self.methodInfoMap[methodId]
        else:
            print(f'Symbol Table Error: method {methodId} not found in symbol table')
            exit(1)


################################################################################################

# Register allocator (one per method)

################################################################################################

class RegAllocator:
    """
    Allocate registers for a single method

    - What registers a variable maps to at each line
    - What variable a register maps to
    """

    def __init__(self, cMtd:'CMtd', symbolTable:'SymbolTable') -> None:
        self.memCnt = INITITAL_STK_SPACE # reserved for values that need to be preserved in a1-a4
        self.cMtd = cMtd
        self.symbolTable = symbolTable

    def allocateReg(self):
        """
        Returns a mapping of var to register at each line
        """
        stmts = self.cMtd.mdBody.stmts
        self.cfg = newCFG(stmts)

        # Generate live range info for all variables
        self.genLiveRanges()

        # Init reg allocation
        self.initRegPool()
        self.allocateFormalArgs()
        stk = [self.cfg.root] # Start allocating from first block
        visited = set()
        # DFS
        while stk:
            block = stk.pop()
            if block.name in visited:
                continue
            visited.add(block.name)
            self.allocateRegToBlock(block)
            for c in block.children:
                stk.append(c)

    def genLiveRanges(self):
        stk = [self.cfg.base]
        visited = set()
        while stk:
            block = stk.pop()
            genBlockInfo(block)

            if block.name in visited:
                continue
            
            visited.add(block.name)
            for p in block.parents:
                stk.append(p)

    def initRegPool(self):
        self.varToReg = {} # Maps var to reg
        self.varToMem = {} # Maps var to mem
        self.regToVar = {} # Maps reg to var
        # self.memToVar = {} # Maps mem to var
        self.stkToVar = {}
        self.usedVRegs = set() # lists the v regs that are used
        self.regPool = ["_v5", "_v4", "_v3", "_v2", "_v1", "_a4", "_a3", "_a2", "_a1"]

    def allocateFormalArgs(self):
        """
        Allocate each formal argument of the method to a register (first 4) or to a mem location
        """
        self.localVarMapping = {}
        for i in range(len(self.cMtd.formals)):
            if i < 4:
                f = self.cMtd.formals[i]
                v = f.id 
                reg = self.regPool.pop()
                self.varToReg[v] = reg
                self.regToVar[reg] = v
                continue

            f = self.cMtd.formals[i]
            v = f.id 
            reg = f'_m{self.memCnt}'
            self.localVarMapping[v] = reg
            self.memCnt += 1

    def allocateRegToBlock(self, b:'Block'):
        b.blockInfo.varToRegPerLine = [{} for i in range(len(b.stmts))]
        b.blockInfo.varToMemPerLine = [dict(self.localVarMapping) for i in range(len(b.stmts))]
        b.blockInfo.regToVarPerLine = [{} for i in range(len(b.stmts))]
        b.blockInfo.stkToVarPerLine = [{} for i in range(len(b.stmts))]
        
        for i in range(len(b.stmts)):
            # # ignore Label stmt
            # if isinstance(b.stmts[i], LabelStmt):
            #     continue

            # # ignore Goto stmt
            # if isinstance(b.stmts[i], GotoStmt):
            #     continue

            # Free registers if there exists some registers that are no longer needed
            
            self.freeRegs(b, i)

            # Assign 'a' registers for call stmts
            if hasCall(b.stmts[i]):
                if isinstance(b.stmts[i], PrintStmt) or isinstance(b.stmts[i], ReadStmt):
                    isRead = isinstance(b.stmts[i], ReadStmt)
                    if isVar(b.stmts[i].id):
                        varType = self.symbolTable.getVarTypeFromMethod(self.cMtd.id, b.stmts[i].id)
                        if varType == INT_TYPE or varType == BOOL_TYPE:
                            formatter = INT_NO_LINE_FORMATTER if isRead else INT_FORMATTER
                        elif varType == STR_TYPE:
                            formatter = STR_FORMATTER
                        else:
                            print(f'Only Int/Bool or Str allowed to be printed (and read) but found {varType}')
                            exit(1)
                    elif isIntLiteral(b.stmts[i].id) or isBoolLiteral(b.stmts[i].id):
                        formatter = INT_NO_LINE_FORMATTER if isRead else INT_FORMATTER
                    elif isStringLiteral(b.stmts[i].id):
                        formatter = STR_FORMATTER
                    else:
                        print(f'Only Int/Bool or Str allowed to be printed (and read) but found {b.stmts[i].id}')
                        exit(1)

                    args = [formatter, b.stmts[i].id]
                    if isBoolLiteral(args[1]):
                        args[1] = "1" if args[1] == "true" else "0"

                elif (isinstance(b.stmts[i], AssignFieldStmt) or isinstance(b.stmts[i], AssignIdStmt) or \
                    isinstance(b.stmts[i], AssignTypeIdStmt)) and "new" in b.stmts[i].exp.items:
                    className = b.stmts[i].exp.items[1] # exp = new Cname ()
                    classSize = self.symbolTable.getClassBodySize(className)
                    args = [str(classSize)]

                else:
                    args = [v for v in b.stmts[i].exp.items] # can be int, str, bool, or another var

                # Free up a1 to a4 (up till the one that is needed)
                stkIdx = 0
                argCnt = len(args)
                for j in range(argCnt):
                    if j < 4:
                        reqReg = f'_a{j+1}'
                        # free the reqReg if it is currently occupied
                        if reqReg in self.regToVar:
                            if self.regToVar[reqReg] == args[j]:
                                continue
                            vToSpill = self.regToVar.pop(reqReg)
                            self.varToReg.pop(vToSpill, None)

                            if isVar(vToSpill):
                                self.getReg(vToSpill, b, i, True)

                        elif reqReg in self.regPool: 
                            self.regPool.remove(reqReg)
                        # Map the variable argument to this register
                        
                        if isVar(args[j]):
                            if args[j] not in self.varToReg:
                                self.varToReg[args[j]] = reqReg
                                self.regToVar[reqReg] = args[j]

                            elif self.varToReg[args[j]] == reqReg:
                                pass
                                
                                # self.varToReg[args[j]] != reqReg:
                                # but there is a chance that the earlier arguments are the same
                            elif self.varToReg[args[j]] != reqReg and \
                                "a" in self.varToReg[args[j]] and \
                                self.varToReg[args[j]] < reqReg: 

                                self.varToReg[args[j]] = reqReg
                                self.regToVar[reqReg] = args[j]

                            else: # self.varToReg[args[j]] != reqReg:
                                regToFree = self.varToReg.pop(args[j])
                                self.regToVar.pop(regToFree, None)
                                self.regPool.append(regToFree)
                                self.varToReg[args[j]] = reqReg
                                self.regToVar[reqReg] = args[j]
                        else:
                            self.regToVar[reqReg] = args[j]
                        
                        continue

                    # function call with more than 4 arguments
                    # | prev top | <- sp
                    # | extra    |
                    # | 6th arg  |
                    # | 5th arg  |
                    stkName = f'_k{stkIdx}'
                    self.stkToVar[stkName] = args[j]
                    stkIdx += 1

                for v in b.blockInfo.defPerLine[i]:
                    self.getReg(v, b, i)

                b.blockInfo.varToRegPerLine[i] = dict(self.varToReg)
                b.blockInfo.varToMemPerLine[i].update(self.varToMem)
                b.blockInfo.stkToVarPerLine[i].update(self.stkToVar)
                b.blockInfo.regToVarPerLine[i].update(self.regToVar)

                # Done updating
                self.stkToVar.clear()
                continue

            # # Delay reg allocation for variables that do not need to be used yet 
            # # - only used some time later (live but NOT IN curr use set)
            # # - not currently defined     (live but NOT IN curr def set)
            currVars = set()
            for v in b.blockInfo.usePerLine[i].union(b.blockInfo.defPerLine[i]):
                currVars.add(v)
            for v in b.blockInfo.livePerLine[i]:
                if v in b.blockInfo.defPerLine[i]:
                    currVars.add(v)
            for v in currVars:
                # For variables that need to be used immediately (and not allocated a register), assign them now
                if v not in self.varToReg:
                    self.getReg(v, b, i)


            b.blockInfo.varToRegPerLine[i] = dict(self.varToReg)
            b.blockInfo.varToMemPerLine[i].update(self.varToMem)
            b.blockInfo.stkToVarPerLine[i].update(self.stkToVar)
            b.blockInfo.regToVarPerLine[i].update(self.regToVar)

    
    def getReg(self, v:'str', b:'Block', i:'int', mustBeV=False):
        if v in self.varToReg:
            return
        # Have available registers
        if mustBeV and self.regPool:
            reg = None
            i = len(self.regPool) - 1
            while i >= 0:
                if "v" in self.regPool[i]:
                    reg = self.regPool[i]
                    self.regPool.remove(reg)
                    break
                i -= 1
            if reg is not None:
                self.varToReg[v] = reg
                self.regToVar[reg] = v
                self.usedVRegs.add(reg)
            return
        if self.regPool:
            reg = self.regPool.pop()
            self.varToReg[v] = reg
            self.regToVar[reg] = v
            if '_v' in reg:
                self.usedVRegs.add(reg)
            return

        # No available registers
        # Spill a local variable HIGHEST NEXT USE back to mem
        candidate = None
        maxNextUse = -1
        for vToSpill in self.varToReg:
            if vToSpill in self.localVarMapping and vToSpill not in b.blockInfo.usePerLine[i] and b.blockInfo.livePerLine[i][vToSpill] > maxNextUse:
                candidate = vToSpill
                maxNextUse = b.blockInfo.livePerLine[i][vToSpill]
        
        if candidate is not None:
            reg = self.varToReg.pop(candidate) # Guaranteed to be in self.regMapping
            self.varToReg[v] = reg
            self.regToVar[reg] = v
            return

        # No local variable available
        # Spill a variable with HIGHEST NEXT USE to mem
        # reserve a slot on stack for this spilled variable
        candidate = None
        maxNextUse = -1
        for vToSpill in self.varToReg:
            if vToSpill not in b.blockInfo.usePerLine[i] and b.blockInfo.livePerLine[i][vToSpill] > maxNextUse:
                candidate = vToSpill
                maxNextUse = b.blockInfo.livePerLine[i][vToSpill]

        # Guaranteed a candidate
        reg = self.varToReg.pop(candidate) # Guaranteed to be in self.regMapping
        self.varToReg[v] = reg
        self.regToVar[reg] = v

        self.varToMem[candidate] = f'_m{self.memCnt}'
        self.memCnt += 1

    def freeRegs(self, b:'Block', i:'int'):
        # Free registers for variables that are not used by scanning vars
        dropSet = []
        for v in self.varToReg:
            if v not in b.blockInfo.livePerLine[i] and v not in b.blockInfo.usePerLine[i] and v not in b.inVars and v not in b.outVars:
                dropSet.append(v)
        for v in dropSet:
            reg = self.varToReg.pop(v, None) 
            self.regToVar.pop(reg, None) 
            if reg is not None:
                self.regPool.append(reg)

        # Same, but scan registers instead
        dropSet = []
        for reg in self.regToVar:
            v = self.regToVar[reg]
            if v not in b.blockInfo.livePerLine[i] and v not in b.blockInfo.usePerLine[i] and v not in b.inVars and v not in b.outVars:
                dropSet.append(reg)
        for reg in dropSet:
            v = self.regToVar.pop(reg, None) 
            self.regPool.append(reg)
            self.varToReg.pop(v, None) 

        # If multiple reg maps to same var, keep the one which the reg maps to
        dropSet = []
        for v in self.varToReg:
            keepReg = self.varToReg[v]
            for reg in self.regToVar:
                if self.regToVar[reg] == v and reg != keepReg:
                    dropSet.append(reg)
        for reg in dropSet:
            v = self.regToVar.pop(reg, None) 
            self.regPool.append(reg)


def genBlockInfo(block:'Block'):
    """
    Returns the live and def set of each line in the block
    """
    block.outVars.update(getLiveOut(block))

    n = len(block.stmts)
    stmtLiveSet = [{} for i in range(n)]
    stmtDefSet = [[] for i in range(n)]
    stmtUseSet = [set() for i in range(n)]
    
    liveVars = {}
    for v in block.outVars:
        liveVars[v] = n # variable is live past the last line of the block

    for i in range(n-1,-1,-1):
        useSet = getUseVarFromStmt(block.stmts[i])
        defSet = getDefVarFromStmt(block.stmts[i])

        stmtLiveSet[i].update(liveVars)
        stmtUseSet[i].update(useSet)
        stmtDefSet[i] = [x for x in defSet]
        for v in defSet:
            liveVars.pop(v, None)
        for v in useSet:
            liveVars[v] = i

    bf = BlockInfo()
    bf.livePerLine = stmtLiveSet
    bf.defPerLine = stmtDefSet
    bf.usePerLine = stmtUseSet
    block.blockInfo = bf

    block.inVars.update(liveVars)

def getLiveOut(block:'Block'):
    """
    Get all vars that are in the live in of the block's chidren 
    """
    liveOut = set()
    for c in block.children:
        liveOut.update(c.inVars)
    return liveOut

def getUseVarFromStmt(s:'Stmt') -> 'set[str]':
    res = set()
    if isinstance(s, IfStmt):
        res.update(getUseVarFromExp(s.relExp))

    elif isinstance(s, PrintStmt):
        res.update(getUseVarFromExp(Exp(s.id)))

    elif isinstance(s, ReadStmt):
        res.update(getUseVarFromExp(Exp(s.id)))

    elif isinstance(s, AssignTypeIdStmt):
        res.update(getUseVarFromExp(s.exp))

    elif isinstance(s, AssignIdStmt):
        res.update(getUseVarFromExp(s.exp))

    elif isinstance(s, AssignFieldStmt):
        res.update(getUseVarFromExp(s.exp))
        res.add(s.classId)

    elif isinstance(s, CallStmt):
        res.update(getUseVarFromExp(s.exp))

    elif isinstance(s, ReturnStmt):
        res.update(getUseVarFromExp(Exp(s.id)))

    return res

def getDefVarFromStmt(s:'Stmt') -> 'set[str]':
    res = set()
    if isinstance(s, ReadStmt):
        res.add(s.id)

    elif isinstance(s, AssignTypeIdStmt):
        res.add(s.id)

    elif isinstance(s, AssignIdStmt):
        res.add(s.id)

    # elif isinstance(s, AssignFieldStmt):
    #     res.add(s.classId)

    return res

def getUseVarFromExp(e:'Exp') -> 'set[str]':
    """
    Returns all var used in an Exp
    """
    res = set()
    if isinstance(e, CallExp):
        for a in e.args:
            if isVar(a):
                res.add(a)

    # RelExp and normal Exp       
    else:
        # Field access
        if len(e.items) == 3 and e.items[1] == ".":
            res.add(e.items[0])
        else:
            for a in e.items:
                if isVar(a):
                    res.add(a)
    
    return res

def hasCall(s:'Stmt') -> bool:
    """
    Returns true if a statement invokes an arm function call. False otherwise

    malloc - new Class() 
    printf - println
    scanf  - readln
    local call
    """
    if isinstance(s, PrintStmt) or isinstance(s, ReadStmt):
        return True

    if isinstance(s, AssignIdStmt) or isinstance(s, AssignTypeIdStmt) or isinstance(s, AssignFieldStmt):
        return isinstance(s.exp, CallExp) or "new" in s.exp.items

    if isinstance(s, CallStmt):
        return True

    return False

def getUnusedReg(usedReg, mustBeV = False) -> 'str':
    """
    Returns any unused reg
    """
    usedRegs = set([reg for reg in usedReg])
    if mustBeV:
        allRegs = set(["_v5", "_v4", "_v3", "_v2", "_v1"])
    else:
        allRegs = set(["_v5", "_v4", "_v3", "_v2", "_v1", "_a4", "_a3", "_a2", "_a1"])
    unusedRegs = allRegs - usedRegs
    return unusedRegs.pop()
