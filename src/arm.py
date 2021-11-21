#!/usr/bin/env python

from ir3 import Program, CMtd, CData
from reg import *
from constants import *

verbose = 0

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
                print()
                print(b, [p.name for p in block.parents], [c.name for c in block.children])
                print("Live in: ", block.inVars)
                for i in range(len(block.stmts)):
                    print(i, block.stmts[i].pprint())
                    print("Live: ", block.blockInfo.livePerLine[i])
                    print("Use : ", block.blockInfo.usePerLine[i])
                    print("Def : ", block.blockInfo.defPerLine[i]) 
                    print("VarR: ", block.blockInfo.varToRegPerLine[i])
                    print("VarM: ", block.blockInfo.varToMemPerLine[i])
                    print("RegV: ", block.blockInfo.regToVarPerLine[i])
                    print("StkV: ", block.blockInfo.stkToVarPerLine[i])
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

        # update fp
        fpOffsetFromSp = (methodInfo.memCnt + len(toPush) - 1) * 4
        addFpLine = ArmInstLine(ARM_ADD)
        addFpLine.addArg("fp")
        addFpLine.addArg("sp")
        addFpLine.addArg(formatIntLiteral(str(fpOffsetFromSp)))
        lines.append(addFpLine)

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
        toMov = {}
        # Move argument variables from a registers to other registers if necessary
        if b.name == "B0" and i == 0:
            currArgs = [f.id for f in self.symbolTable.getMethodInfo(self.currMethodId).cMtd.formals]
            for j in range(min(len(currArgs),4)):
                v = currArgs[j]
                if v not in bf.varToRegPerLine[i]: continue
                oldReg = f'_a{j+1}'
                newReg = bf.varToRegPerLine[i][v]
                if oldReg != newReg:
                    toMov[formatRegName(oldReg)] = formatRegName(newReg)

        lines += self.genMovRegArm(bf, i, toMov)
        lines += self.genLdrRegArm(bf, i)
        if hasCall(stmt):
            lines += self.storeARegs([1,2,3,4], bf, i)

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

    def genMovRegArm(self, bf:'BlockInfo', i:'int', otherRToMov={}) -> 'list[ArmLine]':
        """
        Mov regs to other regs so that live regs can be preserved
        """
        lines = []
        rToMov = {}
        rToMov.update(otherRToMov)
        # Get the list of regs that need to be moved to another reg
        if i > 0:
            for v in bf.varToRegPerLine[i]:
                if v in bf.varToRegPerLine[i-1]:
                    currReg = bf.varToRegPerLine[i][v]
                    prevReg = bf.varToRegPerLine[i-1][v]
                    if prevReg != currReg:
                        rToMov[formatRegName(prevReg)] = formatRegName(currReg)
        
        ordering, cycle = toposort(rToMov)
        newOrdering = []
        if cycle is not None:
            tempReg = getUnusedReg(bf.regToVarPerLine[i])
            tempReg = formatRegName(tempReg)
            v1 = list(cycle.keys())[0]
            newOrdering.append((v1, tempReg))
            v = cycle[v1]
            movOrder = []
            while True:
                if v == v1: break
                movOrder.append(v)
                v = cycle[v]
            movOrder.reverse()
            for v in movOrder:
                newOrdering.append((v, cycle[v]))
            newOrdering.append((tempReg, cycle[v1]))
        else:
            ordering.reverse()
            for v in ordering:
                if v not in rToMov: continue
                newOrdering.append((v, rToMov[v]))

        for t in newOrdering:
            movLine = ArmInstLine(ARM_MOV)
            movLine.addArg(t[1])
            movLine.addArg(t[0])
            movLine.setComment(f'mov value from {t[0]} to {t[1]}')
            lines.append(movLine)
        return lines

    def genLdrRegArm(self, bf:'BlockInfo', i:'int') -> 'list[ArmLine]':
        """
        Ldr regs from mem if they are currently used and not previously defined
        """
        lines = []
        # Get the list of regs that need to be moved to another reg
        if i == 0:
            return lines

        for v in bf.varToRegPerLine[i]:
            if v not in bf.varToRegPerLine[i-1] and v in bf.varToMemPerLine[i]:
                mem = bf.varToMemPerLine[i][v]  # "_m..."
                negOffsetFromFp = str(-int(mem[2:]) * 4)
                currReg = bf.varToRegPerLine[i][v]
                ldrLine = ArmInstLine(ARM_LDR)
                ldrLine.addArg(formatRegName(currReg))
                ldrLine.addArg(f'[fp,{formatIntLiteral(negOffsetFromFp)}]')
                ldrLine.setComment(f'ld value from {mem} to {currReg}')
                lines.append(ldrLine)
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
            reg = formatRegName(bf.varToRegPerLine[i][v])
            cmpLine = ArmInstLine(ARM_CMP)
            cmpLine.addArg(reg)
            cmpLine.addArg(ARM_ZERO) # Check if it is larger than False
            cmpLine.setComment(f'if ( {v} ) goto {labelName}')
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
                reg0 = formatRegName(getUnusedReg(bf.regToVarPerLine[i]))
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(reg0)
                movLine.addArg(formatIntLiteral(arg0))
                lines.append(movLine)
            else: # isVar
                reg0 = formatRegName(bf.varToRegPerLine[i][arg0])

            if isIntLiteral(arg1):
                reg1 = formatIntLiteral(arg1)
            else: # isVar
                reg1 = formatRegName(bf.varToRegPerLine[i][arg1])
            cmpLine = ArmInstLine(ARM_CMP)
            cmpLine.addArg(reg0)
            cmpLine.addArg(reg1)
            cmpLine.setComment(f'if ( {arg0} {op} {arg1} ) goto {labelName}')
            lines.append(cmpLine)

            branchLine = ArmInstLine(relOpToArm(op))
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
        ldrLine1.setComment(f'[readln] %d format specifier')
        lines.append(ldrLine1)

        # ldr a2, =LC0 + write_space_offset
        ldrLine2 = ArmInstLine(ARM_LDR)
        ldrLine2.addArg("a2")
        offset2 = self.dataMap[WRITE_SPACE]
        dataLoc2 = f'={DATA_LABEL} + {offset2}'
        ldrLine2.addArg(dataLoc2)
        ldrLine2.setComment(f'[readln] write address')
        lines.append(ldrLine2)

        # bl scanf
        blLine = ArmInstLine(ARM_BL)
        blLine.addArg(ARM_SCANF)
        lines.append(blLine)

        # ldr a2, =LC0 + write_space_offset
        lines.append(ldrLine2)

        # ldr a2, [a2]
        ldrLine3 = ArmInstLine(ARM_LDR)
        ldrLine3.addArg("a2")
        ldrLine3.addArg(formatDerefReg("a2"))
        ldrLine3.setComment(f'[readln] save scanned integer')
        lines.append(ldrLine3)

        lines += self.loadARegs([3,4], bf, i)
        return lines

    def genPrintStmtArm(self, stmt:'PrintStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []
        arg = stmt.id
        # ldr a1, =LC0 + int_fomatter_offset
        ldrLine1 = ArmInstLine(ARM_LDR)
        ldrLine1.addArg("a1")
        formatter = bf.regToVarPerLine[i]["_a1"]  # e.g. "%s\n"
        offset1 = self.dataMap[formatter]
        dataLoc1 = f'={DATA_LABEL} + {offset1}'
        ldrLine1.addArg(dataLoc1)
        ldrLine1.setComment(f'[println] {formatter} format specifier')
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
        blLine.addArg(ARM_PRINTF)
        lines.append(blLine)

        lines += self.loadARegs([2,3,4], bf, i)
        return lines

    def genAssignIdStmtArm(self, stmt:'AssignIdStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []

        v = stmt.id
        reg = formatRegName(bf.varToRegPerLine[i][v])
        if isinstance(stmt.exp, CallExp):
            lines += self.genCallExpArm(stmt.exp, bf, i)
            movLine = ArmInstLine(ARM_MOV)
            movLine.addArg(reg)
            movLine.addArg("a1")
            movLine.setComment(f'[VarAssign] {v} = {stmt.exp.pprint()}')
            lines.append(movLine)

        elif len(stmt.exp.items) == 3:
            # _e1 = new Object ()
            if "new" in stmt.exp.items:
                # mov a1, #4 @ malloc size
                movLine1 = ArmInstLine(ARM_MOV)
                movLine1.addArg("a1")
                size = bf.regToVarPerLine[i]["_a1"]  # e.g. "8"
                movLine1.addArg(formatIntLiteral(size))
                lines.append(movLine1)

                # bl malloc
                blLine = ArmInstLine(ARM_BL)
                blLine.addArg(ARM_MALLOC)
                lines.append(blLine)

                # mov v1, a1
                movLine2 = ArmInstLine(ARM_MOV)
                movLine2.addArg(reg)
                movLine2.addArg("a1")
                movLine2.setComment(f'[VarAssign] {v} = new {stmt.exp.items[1]} ()')
                lines.append(movLine2)

            # _e1 = _e2 . val
            elif "." in stmt.exp.items:
                objV = stmt.exp.items[0]
                objType = self.symbolTable.getVarTypeFromMethod(self.currMethodId, objV)
                fieldId = stmt.exp.items[2]
                fieldOffset = str(self.symbolTable.getFieldOffsetForClass(objType, fieldId))
                objReg = formatRegName(bf.varToRegPerLine[i][objV])

                ldrLine = ArmInstLine(ARM_LDR)
                ldrLine.addArg(reg)
                ldrLine.addArg(f'[{objReg}, {formatIntLiteral(fieldOffset)}]')
                ldrLine.setComment(f'[VarAssign] {v} = {objV}.{fieldId}')
                lines.append(ldrLine)

            elif isArithOp(stmt.exp.items[1]):
                arg1 = stmt.exp.items[0]
                arg2 = stmt.exp.items[2]
                op = stmt.exp.items[1]

                if isIntLiteral(arg1):
                    reg1 = formatRegName(getUnusedReg(bf.regToVarPerLine[i]))
                    movLine1 = ArmInstLine(ARM_MOV)
                    movLine1.addArg(reg1)
                    movLine1.addArg(formatIntLiteral(arg1))
                    lines.append(movLine1)
                else:
                    reg1 = formatRegName(bf.varToRegPerLine[i][arg1])
                
                if isIntLiteral(arg2):
                    usedRegs = set([k for k in bf.regToVarPerLine[i]]).union(set([f'_{reg1}']))
                    reg2 = formatRegName(getUnusedReg(usedRegs))
                    movLine2 = ArmInstLine(ARM_MOV)
                    movLine2.addArg(reg2)
                    movLine2.addArg(formatIntLiteral(arg2))
                    lines.append(movLine2)
                else:
                    reg2 = formatRegName(bf.varToRegPerLine[i][arg2])

                opLine = ArmInstLine(arithOpToArm(op))
                opLine.addArg(reg)
                if reg == reg1:
                    opLine.addArg(reg2)
                elif reg == reg2:
                    opLine.addArg(reg1)
                else:
                    opLine.addArg(reg1)
                    opLine.addArg(reg2)
                opLine.setComment(f'[VarAssign] {v} = {arg1} {op} {arg2}')
                lines.append(opLine)

            else: # nothing else possible
                print("Error unpacking assignment stmt")
                exit(1)

        # _e1 = - 4 (assign to negative int) / _e1 = - _e1
        elif len(stmt.exp.items) == 2:
            item = stmt.exp.items[1]
            # _e1 = -_e2
            if isVar(item):
                itemReg = formatRegName(bf.varToRegPerLine[i][item]) # _e2
                negLine = ArmInstLine(ARM_NEG)
                negLine.addArg(reg)
                negLine.addArg(itemReg)
                negLine.setComment(f'[VarAssign] {v} = -{item}')
                lines.append(negLine)

            # _e1 = -4
            elif isIntLiteral(item):
                # mov v1, #-4
                intLiteral = "".join(stmt.exp.items)
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(reg)
                movLine.addArg(formatIntLiteral(intLiteral))
                movLine.setComment(f'[VarAssign] {v} = -{item}')
                lines.append(movLine)

        elif len(stmt.exp.items) == 1:
            item = stmt.exp.items[0]
            if isVar(item):
                itemReg = formatRegName(bf.varToRegPerLine[i][item])
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(reg)
                movLine.addArg(itemReg)
                movLine.setComment(f'[VarAssign] {v} = {item}')
                lines.append(movLine)
            elif isIntLiteral(item):
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(reg)
                movLine.addArg(formatIntLiteral(item))
                movLine.setComment(f'[VarAssign] {v} = {item}')
                lines.append(movLine)
            elif isBoolLiteral(item):
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(reg)
                movLine.addArg(formatBoolLiteral(item))
                movLine.setComment(f'[VarAssign] {v} = {item}')
                lines.append(movLine)
            elif isStringLiteral(item):
                ldrLine = ArmInstLine(ARM_LDR)
                ldrLine.addArg(reg)
                offset = self.dataMap[item]
                dataLoc = f'={DATA_LABEL} + {offset}'
                ldrLine.addArg(dataLoc)
                ldrLine.setComment(f'[VarAssign] {v} = {item}')
                lines.append(ldrLine)

        if hasCall(stmt):
            aRegs = []
            for j in range(1,5):
                aReg = f'_a{j}'
                if aReg in bf.regToVarPerLine[i] and \
                    bf.regToVarPerLine[i][aReg] in bf.defPerLine[i]:
                    continue
                aRegs.append(j)
            lines += self.loadARegs(aRegs, bf, i)
        return lines

    def genAssignFieldStmtArm(self, stmt:'AssignFieldStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []
        v = stmt.classId
        classType = self.symbolTable.getVarTypeFromMethod(self.currMethodId, v)
        fieldId = stmt.fieldId
        classFieldOffset = str(self.symbolTable.getFieldOffsetForClass(classType, fieldId))

        reg = formatRegName(bf.varToRegPerLine[i][v])
        tempReg = formatRegName(getUnusedReg(bf.regToVarPerLine[i]))
        if isinstance(stmt.exp, CallExp):
            lines += self.genCallExpArm(stmt.exp, bf, i)
            tempReg = "a1"

        elif len(stmt.exp.items) == 3:
            # _e1 = new Object ()
            if "new" in stmt.exp.items:
                # mov a1, #4 @ malloc size
                movLine1 = ArmInstLine(ARM_MOV)
                movLine1.addArg("a1")
                size = bf.regToVarPerLine[i]["_a1"]  # e.g. "8"
                movLine1.addArg(formatIntLiteral(size))
                lines.append(movLine1)

                # bl malloc
                blLine = ArmInstLine(ARM_BL)
                blLine.addArg(ARM_MALLOC)
                lines.append(blLine)

                # mov v1, a1
                movLine2 = ArmInstLine(ARM_MOV)
                movLine2.addArg(tempReg)
                movLine2.addArg("a1")
                movLine2.setComment(f'[FieldAssign] {tempReg} = new {stmt.exp.items[1]} ()')
                lines.append(movLine2)

            # _e1 = _e2 . val
            elif "." in stmt.exp.items:
                objV = stmt.exp.items[0]
                objType = self.symbolTable.getVarTypeFromMethod(self.currMethodId, objV)
                fieldId = stmt.exp.items[2]
                fieldOffset = str(self.symbolTable.getFieldOffsetForClass(objType, fieldId))
                objReg = formatRegName(bf.varToRegPerLine[i][objV])

                ldrLine = ArmInstLine(ARM_LDR)
                ldrLine.addArg(tempReg)
                ldrLine.addArg(f'[{objReg}, {formatIntLiteral(fieldOffset)}]')
                ldrLine.setComment(f'[FieldAssign] {tempReg} = {objV}.{fieldId}')
                lines.append(ldrLine)

            elif isArithOp(stmt.exp.items[1]):
                arg1 = stmt.exp.items[0]
                arg2 = stmt.exp.items[2]
                op = stmt.exp.items[1]

                if isIntLiteral(arg1):
                    usedRegs = set([k for k in bf.regToVarPerLine[i]]).union(set([f'_{tempReg}']))
                    reg1 = formatRegName(getUnusedReg(usedRegs))
                    movLine1 = ArmInstLine(ARM_MOV)
                    movLine1.addArg(reg1)
                    movLine1.addArg(formatIntLiteral(arg1))
                    lines.append(movLine1)
                else:
                    reg1 = formatRegName(bf.varToRegPerLine[i][arg1])
                
                if isIntLiteral(arg2):
                    usedRegs = set([k for k in bf.regToVarPerLine[i]]).union(set([f'_{reg1}', f'_{tempReg}']))
                    reg2 = formatRegName(getUnusedReg(usedRegs))
                    movLine2 = ArmInstLine(ARM_MOV)
                    movLine2.addArg(reg2)
                    movLine2.addArg(formatIntLiteral(arg2))
                    lines.append(movLine2)
                else:
                    reg2 = formatRegName(bf.varToRegPerLine[i][arg2])

                opLine = ArmInstLine(arithOpToArm(op))
                opLine.addArg(tempReg)
                if tempReg == reg1:
                    opLine.addArg(reg2)
                elif tempReg == reg2:
                    opLine.addArg(reg1)
                else:
                    opLine.addArg(reg1)
                    opLine.addArg(reg2)
                opLine.setComment(f'[FieldAssign] {tempReg} = {arg1} {op} {arg2}')
                lines.append(opLine)

            else: # nothing else possible
                print("Error unpacking assignment stmt")
                exit(1)
                pass

        # _e1 = - 4 (assign to negative int) / _e1 = - _e1
        elif len(stmt.exp.items) == 2:
            item = stmt.exp.items[1]
            # _e1 = -_e2
            if isVar(item):
                itemReg = formatRegName(bf.varToRegPerLine[i][item]) # _e2
                negLine = ArmInstLine(ARM_NEG)
                negLine.addArg(tempReg)
                negLine.addArg(itemReg)
                negLine.setComment(f'[FieldAssign] {tempReg} = -{item}')
                lines.append(negLine)

            # _e1 = -4
            elif isIntLiteral(item):
                # mov v1, #-4
                intLiteral = "".join(stmt.exp.items)
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(tempReg)
                movLine.addArg(formatIntLiteral(intLiteral))
                movLine.setComment(f'[FieldAssign] {tempReg} = -{item}')
                lines.append(movLine)

        elif len(stmt.exp.items) == 1:
            item = stmt.exp.items[0]
            if isVar(item):
                itemReg = formatRegName(bf.varToRegPerLine[i][item])
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(tempReg)
                movLine.addArg(itemReg)
                movLine.setComment(f'[FieldAssign] {tempReg} = {item}')
                lines.append(movLine)
            elif isIntLiteral(item):
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(tempReg)
                movLine.addArg(formatIntLiteral(item))
                movLine.setComment(f'[FieldAssign] {tempReg} = {item}')
                lines.append(movLine)
            elif isBoolLiteral(item):
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(tempReg)
                movLine.addArg(formatBoolLiteral(item))
                movLine.setComment(f'[FieldAssign] {tempReg} = {item}')
                lines.append(movLine)
            elif isStringLiteral(item):
                ldrLine = ArmInstLine(ARM_LDR)
                ldrLine.addArg(tempReg)
                offset = self.dataMap[item]
                dataLoc = f'={DATA_LABEL} + {offset}'
                ldrLine.addArg(dataLoc)
                ldrLine.setComment(f'[FieldAssign] {tempReg} = {item}')
                lines.append(ldrLine)

        strLine = ArmInstLine(ARM_STR)
        strLine.addArg(tempReg)
        strLine.addArg(f'[{reg}, {formatIntLiteral(classFieldOffset)}]')
        strLine.setComment(f'[FieldAssign] {v}.{fieldId} = {tempReg} (temp reg)')
        lines.append(strLine)

        if hasCall(stmt):
            aRegs = []
            for j in range(1,5):
                aReg = f'_a{j}'
                if aReg in bf.regToVarPerLine[i] and \
                    bf.regToVarPerLine[i][aReg] in bf.defPerLine[i]:
                    continue
                aRegs.append(j)
        return lines

    def genCallStmtArm(self, stmt:'CallStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []
        lines += self.genCallExpArm(stmt.exp, bf, i)
        lines += self.loadARegs([1,2,3,4], bf, i)
        return lines

    def genReturnStmtArm(self, stmt:'ReturnStmt', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []
        returnExp = stmt.id
        if isVar(returnExp):
            reg = bf.varToRegPerLine[i][returnExp]
            movLine = ArmInstLine(ARM_MOV)
            movLine.addArg("a1")
            movLine.addArg(formatRegName(reg))
            movLine.setComment(f'return {returnExp}')
            lines.append(movLine)

        elif isStringLiteral(returnExp):
            ldrLine = ArmInstLine(ARM_LDR)
            ldrLine.addArg("a1")
            offset = self.dataMap[returnExp]
            dataLoc = f'={DATA_LABEL} + {offset}'
            ldrLine.addArg(dataLoc)
            ldrLine.setComment(f'return {returnExp}')
            lines.append(ldrLine)

        elif isIntLiteral(returnExp):
            movLine = ArmInstLine(ARM_MOV)
            movLine.addArg("a1")
            movLine.addArg(formatIntLiteral(returnExp))
            movLine.setComment(f'return {returnExp}')
            lines.append(movLine)

        elif isBoolLiteral(returnExp):
            movLine = ArmInstLine(ARM_MOV)
            movLine.addArg("a1")
            movLine.addArg(formatBoolLiteral(returnExp))
            movLine.setComment(f'return {returnExp}')
            lines.append(movLine)

        else: # empty return
            pass
        
        # IR3 optimization already ensures no other statements following return stmt until next block
        branchToExit = ArmInstLine(ARM_B)
        branchToExit.addArg(formatExitLabel(self.currMethodId))
        lines.append(branchToExit)
        return lines

    def genCallExpArm(self, exp:'CallExp', bf:'BlockInfo', i:int) -> 'list[ArmLine]':
        lines = []
        # mov registers
        j = 0
        while j < len(exp.args) and j+1 <= 4:
            reg = f'_a{j+1}'
            arg = bf.regToVarPerLine[i][reg]
        
            if isStringLiteral(arg):
                ldrLine = ArmInstLine(ARM_LDR)
                ldrLine.addArg(formatRegName(reg))
                offset = self.dataMap[arg]
                dataLoc = f'={DATA_LABEL} + {offset}'
                ldrLine.addArg(dataLoc)
                ldrLine.setComment(f'[Call] {reg} = {arg}')
                lines.append(ldrLine)

            elif isIntLiteral(arg):
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(formatRegName(reg))
                movLine.addArg(formatIntLiteral(arg))
                movLine.setComment(f'[Call] {reg} = {arg}')
                lines.append(movLine)

            elif isBoolLiteral(arg):
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(formatRegName(reg))
                movLine.addArg(formatBoolLiteral(arg))
                movLine.setComment(f'[Call] {reg} = {arg}')
                lines.append(movLine)
            j += 1

        j = 0
        # place things on the stack and increment sp
        while j < len(bf.stkToVarPerLine[i]):
            stkPos = reg = f'_k{j}'
            arg = bf.stkToVarPerLine[i][stkPos]
            tempReg = formatRegName(getUnusedReg(bf.regToVarPerLine[i]))

            if isVar(arg):
                if arg in bf.varToRegPerLine[i]: # have been initialized previously
                    vReg = bf.varToRegPerLine[i][arg]
                    movLine = ArmInstLine(ARM_MOV)
                    movLine.addArg(tempReg)
                    movLine.addArg(formatRegName(vReg))
                    lines.append(movLine)

                elif arg in bf.varToMemPerLine[i]:
                    mem = bf.varToMemPerLine[i][arg]  # "_m..."
                    negOffsetFromFp = str(-int(mem[2:]) * 4)
                    ldrLine = ArmInstLine(ARM_LDR)
                    ldrLine.addArg(formatRegName(tempReg))
                    ldrLine.addArg(f'[fp,{formatIntLiteral(negOffsetFromFp)}]')
                    lines.append(ldrLine)

                else:
                    # Var not found in reg or mem mapping
                    # Assign it null value
                    argType = self.symbolTable.getVarTypeFromMethod(self.currMethodId, arg)
                    if argType == STR_TYPE:
                        ldrLine = ArmInstLine(ARM_LDR)
                        ldrLine.addArg(tempReg)
                        offset = self.dataMap[NULL_STRING]
                        dataLoc = f'={DATA_LABEL} + {offset}'
                        ldrLine.addArg(dataLoc)
                        lines.append(ldrLine)
                    else:
                        movLine = ArmInstLine(ARM_MOV)
                        movLine.addArg(tempReg)
                        movLine.addArg(ARM_ZERO)
                        lines.append(movLine)

            elif isStringLiteral(arg):
                ldrLine = ArmInstLine(ARM_LDR)
                ldrLine.addArg(tempReg)
                offset = self.dataMap[arg]
                dataLoc = f'={DATA_LABEL} + {offset}'
                ldrLine.addArg(dataLoc)
                lines.append(ldrLine)

            elif isIntLiteral(arg):
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(tempReg)
                movLine.addArg(formatIntLiteral(arg))
                lines.append(movLine)

            elif isBoolLiteral(arg):
                movLine = ArmInstLine(ARM_MOV)
                movLine.addArg(tempReg)
                movLine.addArg(formatBoolLiteral(arg))
                lines.append(movLine)

            strLine = ArmInstLine(ARM_STR)
            strLine.addArg(tempReg)
            strLine.addArg(f'[sp, {formatIntLiteral(str((j+INITITAL_STK_SPACE+1)*-4))}]')  # e.g. [sp, #-4] [sp, #-8] [sp, #-12].. 
            strLine.setComment(f'[Call] Place additional args on stk')
            lines.append(strLine)

            j+=1

        # adjust sp pointer: sub sp #12
        methodId = exp.methodId
        methodInfo = self.symbolTable.getMethodInfo(methodId)
        methodStkOffset = (methodInfo.memCnt) * 4
        subSPLine = ArmInstLine(ARM_SUB)
        subSPLine.addArg("sp")
        subSPLine.addArg(formatIntLiteral(str(methodStkOffset)))
        subSPLine.setComment(f'[Call] Shift sp to top of stack')
        lines.append(subSPLine)

        # bl method Call
        blLine = ArmInstLine(ARM_BL)
        blLine.addArg(methodId)
        lines.append(blLine)

        # adjust sp pointer back 
        addSPLine = ArmInstLine(ARM_ADD)
        addSPLine.addArg("sp")
        addSPLine.addArg(formatIntLiteral(str(methodStkOffset)))
        addSPLine.setComment(f'[Call] Shift sp back to prev pos (top of frame)')
        lines.append(addSPLine)
        return lines

    def storeARegs(self, aRegs:'list[int]', bf:'BlockInfo', i:int):
        """
        Before a function call is made, all a registers are stored to mem
        """
        lines = []
        # return lines
        for j in aRegs:
            reg = f'_a{j}'
            # if reg not in bf.regToVarPerLine[i]:
            #     continue
            # v = bf.regToVarPerLine[i][reg]
            
            # if isVar(v):
            offset = (j-1) * -4 # #0, #-4, #-8, #-12
            strLine = ArmInstLine(ARM_STR)
            strLine.addArg(formatRegName(reg))
            strLine.addArg(f'[fp,{formatIntLiteral(str(offset))}]')
            strLine.setComment(f'st {formatRegName(reg)} to stack before func call')
            lines.append(strLine)
        return lines

    def loadARegs(self, aRegs:'list[int]', bf:'BlockInfo', i:int):
        """
        After a function call is made, all a registers are restored from mem
        """
        lines = []
        # return lines
        for j in aRegs:
            reg = f'_a{j}'
            # if reg not in bf.regToVarPerLine[i]:
            #     continue
            # v = bf.regToVarPerLine[i][reg]
            
            # if isVar(v):
            offset = (j-1) * -4 # #0, #-4, #-8, #-12
            ldrLine = ArmInstLine(ARM_LDR)
            ldrLine.addArg(formatRegName(reg))
            ldrLine.addArg(f'[fp,{formatIntLiteral(str(offset))}]')
            ldrLine.setComment(f'ld {formatRegName(reg)} original val from stack after func call')
            lines.append(ldrLine)
        return lines


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

def relOpToArm(op:str) -> str:
    return ARM_RELOP_MAPPER[op]

def arithOpToArm(op:str) -> str:
    return ARM_ARITHOP_MAPPER[op]

def toposort(g:'dict[str,str]') -> 'tuple[list[str],dict[str,str]]':
    indeg = {}
    for k in g:
        indeg[k] = 0
        indeg[g[k]] = 0

    for k in g:
        v = g[k]
        indeg[v] += 1

    stk = []
    ordering = []
    for v in indeg:
        if indeg[v] == 0:
            stk.append(v)

    while stk:
        v = stk.pop()
        ordering.append(v)
        if v not in g: continue
        n = g[v]
        indeg[n] -= 1
        if indeg[n] == 0:
            stk.append(n)

    if len(ordering) < len(indeg):
        # cycle exists
        cycle = set([k for k in indeg]) - set(ordering)
        cycleEdges = {}
        for k in cycle:
            cycleEdges[k] = g[k]
        return ordering, cycleEdges

    return ordering, None
    