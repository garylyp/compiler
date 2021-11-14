#!/usr/bin/env python

from os import pipe
from ir3 import Program, CMtd, CData
from reg import *
from constants import *

verbose = False

class ArmLine:
    body:'list[str]'
    comment:str
    def __init__(self) -> None:
        self.body = []
        self.comment = ""

    def setComment(self, comment:str):
        self.comment = comment

    def pprint(self):
        res = ", ".join(self.body)
        if self.comment:
            res = f'{res:<20}@ {self.comment}'
        return res

class ArmEmptyLine(ArmLine):
    """
    Just an empty line
    """
    def __init__(self) -> None:
        pass

    def pprint(self):
        res = ""
        return res

class ArmDirectiveLine(ArmLine):
    """
    .text
    .asciz
    .data
    
    """
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def addArg(self, arg):
        self.body.append(arg)

    def pprint(self):
        res = f'    .{self.name:<7}'
        if self.body:
            res = res + "    " + super().pprint()
        return res

class ArmLabelLine(ArmLine):
    """
    .text
    .asciz
    .data
    
    """
    def __init__(self, labelName) -> None:
        super().__init__()
        self.labelName = labelName

    def pprint(self):
        res = f'{self.labelName}:'
        if self.body:
            res = res + "    " + super().pprint()
        return res

class ArmInstLine(ArmLine):
    """
    mov
    add
    sub
    stmfd
    ldmfd
    
    """
    def __init__(self, instruction:str) -> None:
        super().__init__()
        self.instruction = instruction

    def addArg(self, arg):
        self.body.append(arg)

    def pprint(self):
        res = f'    {self.instruction:<7}'
        if self.body:
            res = res + "    " + super().pprint()
        return res
        

class ArmGenerator:
    def __init__(self, program:'Program') -> None:
        self.program = program
        self.symbolTable = None
        self.dataLines = None
        self.textLines = None

    def genArm(self):
        self.program.cMtdList[0].id = "main"
        self.symbolTable = self.genSymbolTable()
        self.dataLines = self.genData()
        self.textLines = self.genText()

        lines = []
        lines += self.dataLines
        lines.append(ArmEmptyLine())
        lines += self.textLines
        for line in lines:
            print(line.pprint())

    def genSymbolTable(self):
        classes = set([cd.cname for cd in self.program.cDataList])
        st = SymbolTable()
        for cd in self.program.cDataList:
            cname = cd.cname
            classInfo = self.genClassStackInfo(cd, classes)
            st.addClassInfo(cname, classInfo)
        
        for cm in self.program.cMtdList:
            st.populateVarStackInfo(cm)
        return st

    def genClassStackInfo(self, cData:'CData', classes:'set[str]') -> 'ClassStackInfo':
        classInfo = ClassStackInfo(cData.cname, PTR_SIZE)
        for vd in cData.varDecl:
            if vd.type == INT_TYPE:
                classInfo.addField(vd.id, INT_SIZE)
            elif vd.type == STR_TYPE:
                classInfo.addField(vd.id, STR_SIZE)
            elif vd.type == BOOL_TYPE:
                classInfo.addField(vd.id, BOOL_SIZE)
            elif vd.type in classes:
                classInfo.addField(vd.id, PTR_SIZE)
            else:
                print(f'Arm Gen Error: type {vd.type} of class field {cData.cname}.{vd.id} ' + \
                    f'not found while generating symbol table')
                exit(1)
        return classInfo
    

    def genData(self) -> 'list[ArmLine]':
        lines = []
        lines.append(ArmDirectiveLine("data"))
        lines.append(ArmLabelLine(DATA_LABEL))

        self.dataMap = {}
        self.dataOffset = 0

        preDefault = [
            INT_NO_LINE_FORMATTER,
            INT_FORMATTER,
            STR_FORMATTER,
            NULL_STRING,
            WRITE_SPACE,
        ]
        for s in preDefault:
            self.addAscizToData(s)
            line = ArmDirectiveLine("asciz")
            line.setComment(f'{self.dataMap[s]}')
            line.addArg(s)
            lines.append(line)

        strings = set()
        for m in self.program.cMtdList:
            for s in m.mdBody.stmts:
                strings.update(getAsciiFromStmt(s))
        for s in strings:
            self.addAscizToData(s)
            line = ArmDirectiveLine("asciz")
            line.setComment(f'{self.dataMap[s]}')
            line.addArg(s)
            lines.append(line)
        return lines
    
    def addAscizToData(self, ascizString:str):
        self.dataMap[ascizString] = self.dataOffset
        # include null char, minus inverted commas
        offset = len(ascizString) + 1 - 2
        offset -= ascizString.count("\\")
        self.dataOffset += offset

    def genText(self) -> 'list[ArmLine]':
        lines = []
        lines.append(ArmDirectiveLine("text"))

        mainMtd = self.program.cMtdList[0]
        globalMain = ArmDirectiveLine("global")
        globalMain.addArg(mainMtd.id)
        lines.append(globalMain)

        typeMain = ArmDirectiveLine("type")
        typeMain.addArg(mainMtd.id)
        typeMain.addArg("%function")
        lines.append(typeMain)

        for i in range(0, len(self.program.cMtdList)):
            # include label, and all inst lines
            cMtd = self.program.cMtdList[i]
            regAlloc = self.allocateReg(cMtd)
            methodId = cMtd.id
            self.symbolTable.addMethodInfo(methodId, regAlloc)

        for i in range(0, len(self.program.cMtdList)):
            cMtd = self.program.cMtdList[i]
            methodInfo = self.symbolTable.getMethodInfo(cMtd.id)
            lines += self.genMtdArm(methodInfo)
            lines.append(ArmEmptyLine())

        return lines

    def allocateReg(self, cMtd:'CMtd') -> 'RegAllocator':
        r = RegAllocator(cMtd, self.symbolTable)
        r.allocateReg()
        for b in r.cfg.blockMap:
            block = r.cfg.blockMap[b]
            if verbose:
                # print()
                # print(b, [p.name for p in block.parents], [c.name for c in block.children])
                # print("Live in: ", block.inVars)
                # for i in range(len(block.stmts)):
                #     print(i, block.stmts[i].pprint())
                #     print("Live: ", block.blockInfo.livePerLine[i])
                #     print("Use : ", block.blockInfo.usePerLine[i])
                #     print("Def : ", block.blockInfo.defPerLine[i]) 
                #     print("VarR: ", block.blockInfo.varToRegPerLine[i])
                #     print("VarM: ", block.blockInfo.varToMemPerLine[i])
                #     print("RegV: ", block.blockInfo.regToVarPerLine[i])
                #     print("StkV: ", block.blockInfo.stkToVarPerLine[i])
                print("Live out: ", block.outVars)
        return r

    def genMtdArm(self, methodInfo:'RegAllocator') -> 'list[ArmLine]':
        lines = []
        
        # Use methodId as label
        self.currMethodId = methodInfo.cMtd.id
        methodLabel = ArmLabelLine(self.currMethodId)
        lines.append(methodLabel)

        # Store callee registers on stack
        usedVRegs = [formatRegName(reg) for reg in methodInfo.usedVRegs]
        usedVRegs.sort() # v1 v2 v3 v4 v5

        toPush = ["fp", "lr"]
        toPush += usedVRegs
        stmfdLine = ArmInstLine(ARM_STMFD)
        stmfdLine.addArg("sp!")
        stmfdLine.addArg("{%s}" % ",".join(toPush))
        lines.append(stmfdLine)

        for blockName in methodInfo.cfg.blockMap:
            block = methodInfo.cfg.blockMap[blockName]
            lines += self.genBlockArm(block)


        exitLabel = ArmLabelLine(formatExitLabel(self.currMethodId))
        lines.append(exitLabel)

        toPop = [r for r in toPush]
        toPop[1] = "pc"
        ldmfdLine = ArmInstLine(ARM_LDMFD)
        ldmfdLine.addArg("sp!")
        ldmfdLine.addArg("{%s}" % ",".join(toPop))
        lines.append(ldmfdLine)
        return lines

    def genBlockArm(self, b:'Block') -> 'list[ArmLine]':
        lines = []
        for i in range(len(b.stmts)):
            lines += self.genStmtArm(b, i)

        return lines
            

    def genStmtArm(self, b:'Block', i:int)  -> 'list[ArmLine]':
        lines = []

        stmt = b.stmts[i]
        bf = b.blockInfo
        # should re-update variables that were used in earlier lines but change regs in this line
        # mov ...
        # mov ...

        if isinstance(stmt, LabelStmt):
            lines += self.genLabelStmtArm(stmt, bf, i)

        elif isinstance(stmt, GotoStmt):
            lines += self.genGotoStmtArm(stmt, bf, i)

        elif isinstance(stmt, IfStmt):
            lines += self.genIfStmtArm(stmt, bf, i)

        elif isinstance(stmt, ReadStmt):
            lines += self.genReadStmtArm(stmt, bf, i)

        elif isinstance(stmt, PrintStmt):
            lines += self.genPrintStmtArm(stmt, bf, i)

        elif isinstance(stmt, AssignTypeIdStmt) or isinstance(stmt, AssignIdStmt):
            lines += self.genAssignIdStmtArm(stmt, bf, i)

        elif isinstance(stmt, AssignFieldStmt):
            lines += self.genAssignFieldStmtArm(stmt, bf, i)

        elif isinstance(stmt, CallStmt):
            lines += self.genCallStmtArm(stmt, bf, i)

        elif isinstance(stmt, ReturnStmt):
            lines += self.genReturnStmtArm(stmt, bf, i)

        return lines

    def genLabelStmtArm(self, stmt:'LabelStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []
        labelName = f'.L{stmt.labelNum}'
        lines.append(ArmLabelLine(labelName))
        return lines

    def genGotoStmtArm(self, stmt:'GotoStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []
        labelName = f'.L{stmt.labelNum}'
        branchLine = ArmInstLine(ARM_B)
        branchLine.addArg(labelName)
        lines.append(branchLine)
        return lines

    def genIfStmtArm(self, stmt:'IfStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []
        labelName = f'.L{stmt.labelNum}'

        # if ( _e1 ) { ... }
        if len(stmt.relExp.items) == 1:
            v = stmt.relExp.items[0]
            reg = bf.varToRegPerLine[i][v]
            cmpLine = ArmInstLine(ARM_CMP)
            cmpLine.addArg(reg)
            cmpLine.addArg(ARM_ZERO) # Check if it is larger than False
            lines.append(cmpLine)

            bgtLine = ArmInstLine(ARM_BGT)
            bgtLine.addArg(labelName)
            lines.append(bgtLine)

        # if ( _a1 > 3 )
        else:
            arg0 = stmt.relExp.items[0]
            arg1 = stmt.relExp.items[2]
            op = stmt.relExp.items[1]
            if isIntLiteral(arg0):
                reg0 = getUnusedReg(bf.regToVarPerLine[i])
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(reg0)
                movLine.addArg(formatIntLiteral(arg0))
                lines.append(movLine)
            else: # isVar
                reg0 = bf.varToRegPerLine[i][arg0]

            if isIntLiteral(arg1):
                reg1 = formatIntLiteral(arg1)
            else: # isVar
                reg1 = bf.varToRegPerLine[i][arg1]
            cmpLine = ArmInstLine(ARM_CMP)
            cmpLine.addArg(reg0)
            cmpLine.addArg(reg1)
            lines.append(cmpLine)

            branchLine = ArmInstLine(resolveRelOpToArmInst(op))
            branchLine.addArg(labelName)
            lines.append(branchLine)
        return lines

    def genReadStmtArm(self, stmt:'ReadStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []
        arg = stmt.id
        # ldr a1, =LC0 + int_fomatter_offset
        ldrLine1 = ArmInstLine(ARM_LDR)
        ldrLine1.addArg("a1")
        formatter = bf.regToVarPerLine[i]["_a1"]  # "%d"
        offset1 = self.dataMap[formatter]
        dataLoc1 = f'={DATA_LABEL} + {offset1}'
        ldrLine1.addArg(dataLoc1)
        lines.append(ldrLine1)

        # ldr a2, =LC0 + write_space_offset
        ldrLine2 = ArmInstLine(ARM_LDR)
        ldrLine2.addArg("a2")
        offset2 = self.dataMap[WRITE_SPACE]
        dataLoc2 = f'={DATA_LABEL} + {offset2}'
        ldrLine2.addArg(dataLoc2)
        lines.append(ldrLine2)

        # bl scanf
        blLine = ArmInstLine(ARM_BL)
        blLine.addArg("scanf")
        lines.append(blLine)

        # ldr a2, =LC0 + write_space_offset
        lines.append(ldrLine2)

        # ldr a2, [a2]
        ldrLine3 = ArmInstLine(ARM_LDR)
        ldrLine3.addArg("a2")
        ldrLine3.addArg(formatDerefReg("a2"))
        lines.append(ldrLine3)

        return lines

    def genPrintStmtArm(self, stmt:'PrintStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []
        arg = stmt.id
        # ldr a1, =LC0 + int_fomatter_offset
        ldrLine1 = ArmInstLine(ARM_LDR)
        ldrLine1.addArg("a1")
        formatter = bf.regToVarPerLine[i]["_a1"]  # "%s\n"
        offset1 = self.dataMap[formatter]
        dataLoc1 = f'={DATA_LABEL} + {offset1}'
        ldrLine1.addArg(dataLoc1)
        lines.append(ldrLine1)

        if isVar(arg):
            pass # no need to handle cos alr done
        
        elif isStringLiteral(arg):
            ldrLine = ArmInstLine(ARM_LDR)
            ldrLine.addArg("a2")
            offset = self.dataMap[arg]
            dataLoc = f'={DATA_LABEL} + {offset}'
            ldrLine.addArg(dataLoc)
            lines.append(ldrLine)

        elif isIntLiteral(arg):
            movLine = ArmInstLine(ARM_MOV)
            movLine.addArg("a2")
            movLine.addArg(formatIntLiteral(arg))
            lines.append(movLine)

        # bl printf
        blLine = ArmInstLine(ARM_BL)
        blLine.addArg("printf")
        lines.append(blLine)
        return lines

    def genAssignIdStmtArm(self, stmt:'AssignIdStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []

        return lines

    def genAssignFieldStmtArm(self, stmt:'AssignFieldStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []

        return lines

    def genCallStmtArm(self, stmt:'CallStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []

        return lines

    def genReturnStmtArm(self, stmt:'ReturnStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []
        returnExp = stmt.id
        if isVar(returnExp):
            # TODO: load from mem if not found in reg
            reg = bf.varToRegPerLine[i][returnExp]
            movLine = ArmInstLine(ARM_MOV)
            movLine.addArg("a1")
            movLine.addArg(reg)
            lines.append(movLine)

        elif isStringLiteral(stmt.id):
            ldrLine = ArmInstLine(ARM_LDR)
            ldrLine.addArg("a1")
            offset = self.dataMap[stmt.id]
            dataLoc = f'={DATA_LABEL} + {offset}'
            ldrLine.addArg(dataLoc)
            lines.append(ldrLine)

        elif isIntLiteral(stmt.id):
            movLine = ArmInstLine(ARM_MOV)
            movLine.addArg("a1")
            movLine.addArg(formatIntLiteral(stmt.id))
            lines.append(movLine)

        elif isBoolLiteral(stmt.id):
            movLine = ArmInstLine(ARM_MOV)
            movLine.addArg("a1")
            movLine.addArg(formatBoolLiteral(stmt.id))
            lines.append(movLine)

        else: # empty return
            pass
        
        # IR3 optimization already ensures no other statements following return stmt until next block
        # branchToExit = ArmInstLine(ARM_UNCOND_BRANCH)
        # branchToExit.addArg(formatExitLabel(self.currMethodId))
        # lines.append(branchToExit)
        return lines

    def genExpArm(self, exp:'Exp', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        if isinstance(exp, CallExp):
            return self.genCallExpArm(exp, bf, i)

    def genRelExpArm(self, exp:'RelExp', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        pass



def isAsciiString(literal:str):
    return re.match(r"\".*\"", literal) is not None
        
def getAsciiFromStmt(s:'Stmt'):
    asciiStrings = []
    if isinstance(s, PrintStmt) or isinstance(s, ReturnStmt):
        if isAsciiString(s.id):
            asciiStrings.append(s.id)

    if isinstance(s, AssignFieldStmt) or isinstance(s, AssignIdStmt) or isinstance(s, AssignTypeIdStmt) or isinstance(s, CallStmt): 
        for e in s.exp.items:
            if isAsciiString(e):
                asciiStrings.append(e)
    
    return asciiStrings

def formatRegName(raw:str) -> str:
    """
    _a1 --> a1;
    _v1 --> v1;
    """
    if "_" in raw:
        return raw[1:]
    return raw

def formatIntLiteral(raw:str) -> str:
    return "#" + raw

def formatBoolLiteral(raw:str) -> str:
    if raw == "true":
        return ARM_ONE
    else: # raw == "false":
        return ARM_ZERO

def formatExitLabel(methodId:str) -> str:
    return f'.{methodId}_exit'

def formatDerefReg(reg:str) -> str:
    return f'[{reg}]'

def resolveRelOpToArmInst(op:str) -> str:
    return ARM_RELOP_MAPPER[op]