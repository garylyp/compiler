from cfg import CFG, Block
from ir3 import *

NON_VAR_SYMBOLS = {"true", "false", "+", "-", "*", "/", ">", ">=", "<", "<=", "==", "!=", "."}

class RegManager:
    """
    Contains information about
    - What registers are available for use
    - What registers a variable maps to
    - What variable a register maps to
    """
    def __init__(self) -> None:
        self.scratchRegs = ["v1", "v2", "v3", "v4", "v5"]
        self.regToVar = {}
        self.varToReg = {}
        
    def getReg(self, var):
        if var in self.varToReg:
            return self.varToReg[var]
        
        reg = self.allocateReg()
        self.varToReg[var] = reg
        return reg

    def allocateReg(self):
        """
        Get next available scratch register. If none available, spill existing
        """
        if self.scratchRegs:
            reg = self.scratchRegs.pop(0)
            return reg

        #TODO spilling heuristic



class VarLiveRange:
    """
    Contains mapping of a variable's live range in a method
    """
    varLocalRange:'dict[str,set[str]]'
    varGlobalRange:'dict[str,set[str]]'
    def __init__(self) -> None:
        self.varLocalRange = {}
        self.varGlobalRange = {}

    def addLineIdToVar(self, var, lineId):
        if var in self.varLocalRange:
            self.varLocalRange[var].add(lineId)
        else:
            self.varLocalRange[var] = { lineId }

    def addBlockNameToVar(self, var, blockname):
        if var in self.varGlobalRange:
            self.varGlobalRange[var].add(blockname)
        else:
            self.varGlobalRange[var] = { blockname }

class RegAllocator:
    def getLiveRangeInfo(self, cfg:'CFG') -> VarLiveRange:
        v = VarLiveRange()
        for blockName in cfg.blockMap:
            block = cfg.blockMap[blockName]
            block.inVars = getLiveIn(block)

        for blockName in cfg.blockMap:
            block = cfg.blockMap[blockName]
            block.outVars = getLiveOut(block)
        return v


    def getBlockLiveRangeInfo(self, block:'Block'):
        n = len(block.stmts)
        stmtLiveSet = [{} for i in range(n)]
        
        liveVars = {}
        liveVars.update(block.outVars)
        # Get live out
        for i in range(n-1,-1,-1):
            useSet = getUseVarFromStmt(block.stmts[i])
            defSet = getDefVarFromStmt(block.stmts[i])

            liveVars = liveVars - defSet
            liveVars.update(useSet)
            stmtLiveSet[i].update(liveVars)
            




def getLiveIn(block:'Block'):
    """
    Get all vars that are used in Block but not defined in block
    """
    n = len(block.stmts)
    useSet = {}
    defSet = {}
    for i in range(n):
        stmt = block.stmts[i]
        useSet.update(getUseVarFromStmt(stmt))
        defSet.update(getDefVarFromStmt(stmt))

    return useSet - defSet

def getLiveOut(block:'Block'):
    """
    Get all vars that are in the live in of the block's chidren 
    """
    liveOut = {}
    for c in block.children:
        liveOut.update(c.inVars)
    return liveOut

def getUseVarFromStmt(s:'Stmt') -> 'set[str]':
    res = set()
    if isinstance(s, IfStmt):
        res.update(getUseVarFromExp(s.relExp))

    elif isinstance(s, PrintStmt):
        res.add(s.id)

    elif isinstance(s, AssignTypeIdStmt):
        res.update(getUseVarFromExp(s.exp))

    elif isinstance(s, AssignIdStmt):
        res.update(getUseVarFromExp(s.exp))

    elif isinstance(s, AssignFieldStmt):
        res.update(getUseVarFromExp(s.exp))

    elif isinstance(s, CallStmt):
        res.update(getUseVarFromExp(s.callExp))

    elif isinstance(s, ReturnStmt):
        res.add(s.id)

    return res

def getDefVarFromStmt(s:'Stmt') -> 'set[str]':
    res = set()
    if isinstance(s, ReadStmt):
        res.add(s.id)

    elif isinstance(s, AssignTypeIdStmt):
        res.add(s.id)

    elif isinstance(s, AssignIdStmt):
        res.add(s.id)

    elif isinstance(s, AssignFieldStmt):
        res.add(s.classId)

    return res

def getUseVarFromExp(e:'Exp') -> 'set[str]':
    """
    Returns all var used in an Exp
    """
    res = set()
    if isinstance(e, CallExp):
        for a in e.args:
            if a not in NON_VAR_SYMBOLS:
                res.add(a)

    # RelExp and normal Exp       
    else:
        for a in e.items:
            if a not in NON_VAR_SYMBOLS:
                res.add(a)
    
    return res