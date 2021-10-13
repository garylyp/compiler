#!/usr/bin/env python

import sys, copy, re
from parse import Parser
from ast2 import *

class Program:
    cDataList:'list[CData]'
    cMtdList:'list[CMtd]'
    def __init__(self, cDataList:'list[CData]', cMtdList:'list[CMtd]') -> None:
        self.cDataList = cDataList
        self.cMtdList = cMtdList
    
    def pprint(self):
        res = ""
        res += "======= CData3 ======="
        res += "\n\n"
        for cData in self.cDataList:
            res += cData.pprint()
            res += "\n\n"

        res += "=======  CMtd3 ======="
        res += "\n"
        for cMtd in self.cMtdList:
            res += cMtd.pprint()
            res += "\n\n"
        return res

class CData:
    cname:str
    varDecl:'list[VarDecl]'

    def __init__(self, cname) -> None:
        self.cname = cname
        self.varDecl = []

    def addVarDecl(self, type, id):
        self.varDecl.append(VarDecl(type, id))

    def pprint(self):
        res = f'class {self.cname} {{ \n'
        # Print field declaration
        for vd in self.varDecl:
            res = res + f'  {vd.pprint()};\n'
        res = res + f'}}'
        return res

class CMtd:
    type:str
    id:str
    formals:'list[VarDecl]'
    mdBody:'MdBody'

    def __init__(self, id, type) -> None:
        self.id = id
        self.type = type
        self.formals = []

    def addFormal(self, type, id):
        self.formals.append(VarDecl(type, id))

    def setMdBody(self, mdBody:'MdBody'):
        self.mdBody = mdBody

    def pprint(self):
        # print formals
        formalListStr = ""
        for i in range(len(self.formals)):
            formalListStr += self.formals[i].pprint()
            if i < len(self.formals) - 1:
                formalListStr += ","

        res = f'{self.type} {self.id}({formalListStr}) {{ \n'
        res += self.mdBody.pprint()
        res = res + f'}}'
        return res

class MdBody:
    varDecl:'list[VarDecl]'
    stmts:'list[Stmt]'

    def __init__(self) -> None:
        self.varDecl = []
        self.stmts = []

    def addVarDecl(self, type, id):
        self.varDecl.append(VarDecl(type, id))

    def addStmt(self, stmt:'Stmt'):
        self.stmts.append(stmt)

    def pprint(self):
        res = ""
        for vd in self.varDecl:
            res = res + f'  {vd.pprint()};\n'
        for s in self.stmts:
            res = res + f'{s.pprint()}\n'
        return res

class VarDecl:
    type:str
    id:str
    def __init__(self, type, id) -> None:
        self.type = type
        self.id = id
    
    def pprint(self):
        return f'{self.type} {self.id}'


class Stmt:
    def __init__(self) -> None:
        pass
    def pprint(self):
        res = "  pprint undefined"
        return res

class LabelStmt(Stmt):
    labelNum:int
    def __init__(self, labelNum):
        self.labelNum = labelNum

    def pprint(self):
        res = f'  Label {self.labelNum}:'
        return res

class IfStmt(Stmt):
    labelNum:int
    relExp:'RelExp'
    def pprint(self):
        res = f'    if ( {self.relExp.pprint()} ) goto {self.labelNum};'
        return res

class GotoStmt(Stmt):
    labelNum:int
    def __init__(self, labelNum) -> None:
        self.labelNum = labelNum

    def pprint(self):
        res = f'    goto {self.labelNum};'
        return res

class ReadStmt(Stmt):
    id:str
    def __init__(self, id:str) -> None:
        self.id = id
    def pprint(self):
        res = f'    readln({self.id});'
        return res

class PrintStmt(Stmt):
    id:str
    """
    id can be constant or id3
    """
    def __init__(self, id:str) -> None:
        self.id = id
    def pprint(self):
        res = f'    println({self.id});'
        return res


class AssignTypeIdStmt(Stmt):
    id:str
    exp:'Exp'
    def __init__(self, type:str, id:str, exp:'Exp') -> None:
        self.type = type
        self.id = id
        self.exp = exp
    def pprint(self):
        res = f'    {self.type} {self.id} = {self.exp.pprint()};'
        return res

class AssignIdStmt(Stmt):
    id:str
    exp:'Exp'
    def __init__(self, id:str, exp:'Exp') -> None:
        self.id = id
        self.exp = exp
    def pprint(self):
        res = f'    {self.id} = {self.exp.pprint()};'
        return res

class AssignFieldStmt(Stmt):
    classId:str
    fieldId:str
    exp:'Exp'
    def __init__(self, classId:str, fieldId:str, exp:'Exp') -> None:
        self.classId = classId
        self.fieldId = fieldId
        self.exp = exp
    def pprint(self):
        res = f'    {self.classId}.{self.fieldId} = {self.exp.pprint()};'
        return res

class CallStmt(Stmt):
    callExp:'CallExp'
    def __init__(self, callExp:'CallExp') -> None:
        self.callExp = callExp
    def pprint(self):
        res = f'    {self.callExp.pprint()};'
        return res

class ReturnStmt(Stmt):
    id:str
    def __init__(self, id:str) -> None:
        self.id = id
    def pprint(self):
        res = f'    return {self.id};'
        return res

class Exp:
    items:'list[str]'
    def __init__(self, *items) -> None:
        self.items = list(items)

    def pprint(self):
        res = " ".join(self.items)
        return res

class RelExp(Exp):
    items:'list[str]'
    def __init__(self, *items) -> None:
        self.items = list(items)

    def pprint(self):
        res = " ".join(self.items)
        return res

class CallExp(Exp):
    methodId:str
    args:'list[str]'
    def __init__(self, methodId:str, args:'list[str]') -> None:
        self.methodId = methodId
        self.args = args
        self.items = args

    def pprint(self):
        res = f'{self.methodId}('
        for i in range(len(self.args)):
            res += self.args[i]
            if i != len(self.args)-1:
                res += ","
        res += ")"
        return res

class Generator:
    ast:AST
    program:Program
    nextMtdId:'dict[str, int]'
    nextLabelNum:int
    nextTempIdNum:int
    methodMap:'dict[str,dict[str,dict[tuple,str]]]' # maps cname -> methodId -> argTypes -> newId

    def __init__(self, ast:AST) -> None:
        self.ast = ast
        self.nextMtdId = {}
        self.nextLabelNum = 0
        self.nextTempIdNum = 0
        self.methodMap = {}

    ################################################################################################

    # Supporting methods

    ################################################################################################

    def nextLabel(self) -> int:
        """
        Returns the next label number
        """
        res = int(self.nextLabelNum)
        self.nextLabelNum += 1
        return res

    def nextTempId(self) -> str:
        """
        Returns the next temp id 
        """
        id = int(self.nextTempIdNum)
        res = f'_e{id}'
        self.nextTempIdNum += 1
        return res

    def argListToArgTypes(self, cname:str, args:'list[VariableNode]') -> 'tuple[str]':
        argTypeList = [cname]
        for a in args:
            argTypeList.append(a.type)
        argTypes = tuple(argTypeList)
        return argTypes

    def storeMethodId(self, cname:str, methodId:str, args:'list[VariableNode]', newId:str):
        argTypes = self.argListToArgTypes(cname, args)
        if cname in self.methodMap:
            if methodId in self.methodMap[cname]:
                self.methodMap[cname][methodId][argTypes] = newId
            else:
                self.methodMap[cname][methodId] = {argTypes : newId}
        else:
            self.methodMap[cname] = {methodId : {argTypes : newId} }
    
    def getMethodId(self, cname:str, methodId:str, argTypes:'tuple[str]'):
        return self.methodMap[cname][methodId][argTypes]

    def getMethodIdByFormals(self, cname:str, methodId:str, args:'list[VariableNode]'):
        argTypes = self.argListToArgTypes(cname, args)
        return self.methodMap[cname][methodId][argTypes]

    ################################################################################################

    # Touching Up / Final Print

    ################################################################################################

    def printIR3(self):
        print(self.program.pprint())

    def trimLabels(self):
        
        for m in self.program.cMtdList:
            newLabelMap = {}
            stmts = m.mdBody.stmts
            for i in range(len(stmts)):
                if isinstance(stmts[i], LabelStmt) and \
                   i + 1 < len(stmts) and isinstance(stmts[i+1], GotoStmt):
                   newLabelMap[stmts[i].labelNum] = stmts[i+1].labelNum
            for i in range(len(stmts)):
                if isinstance(stmts[i], GotoStmt) or isinstance(stmts[i], IfStmt):
                    stmts[i].labelNum = self.getLeaf(newLabelMap, stmts[i].labelNum)


            usedLabels = set()
            for s in m.mdBody.stmts:
                if isinstance(s, IfStmt) or isinstance(s, GotoStmt):
                    usedLabels.add(s.labelNum)

            # Trim unused LabelStmt
            n = len(m.mdBody.stmts)
            i = 0
            while i < n:
                if isinstance(m.mdBody.stmts[i], LabelStmt):
                    if m.mdBody.stmts[i].labelNum not in usedLabels:
                        m.mdBody.stmts.pop(i)
                        n -= 1
                    else:
                        i += 1
                else:
                    i += 1
        
            # Trim unreachable GotoStmt
            n = len(m.mdBody.stmts)
            i = 0
            isPrevStmtGoto = False
            while i < n:
                if isinstance(m.mdBody.stmts[i], GotoStmt):
                    if isPrevStmtGoto:
                        m.mdBody.stmts.pop(i)
                        n -= 1
                    else:
                        isPrevStmtGoto = True
                        i += 1
                else:
                    isPrevStmtGoto = False
                    i += 1
            
    def getLeaf(self, map, id):
        while id in map:
            id = map[id]
        return id


    def backpatch(self):
        self.nextLabelNum = 0        

        oldToNewLabel = {}

        for m in self.program.cMtdList:
            oldToNewTempId = {}
            self.nextTempIdNum = 0
            mdBody = m.mdBody
            for s in mdBody.stmts:
                if isinstance(s, LabelStmt):
                    oldToNewLabel[s.labelNum] = self.nextLabel()

                if isinstance(s, AssignTypeIdStmt):
                    oldToNewTempId[s.id] = self.nextTempId()

            for s in mdBody.stmts:
                if isinstance(s, LabelStmt):
                    s.labelNum = oldToNewLabel[s.labelNum]

                if isinstance(s, IfStmt):
                    s.labelNum = oldToNewLabel[s.labelNum]

                if isinstance(s, GotoStmt):
                    s.labelNum = oldToNewLabel[s.labelNum]


                if isinstance(s, AssignTypeIdStmt) or \
                   isinstance(s, AssignIdStmt) or \
                   isinstance(s, PrintStmt) or \
                   isinstance(s, ReadStmt) or \
                   isinstance(s, ReturnStmt):
                    if s.id in oldToNewTempId: 
                        s.id = oldToNewTempId[s.id]

                if isinstance(s, AssignFieldStmt):
                    if s.classId in oldToNewTempId:
                        s.classId = oldToNewTempId[s.classId]
                
                if isinstance(s, AssignTypeIdStmt) or \
                   isinstance(s, AssignIdStmt) or \
                   isinstance(s, AssignFieldStmt):
                    for i in range(len(s.exp.items)):
                        if s.exp.items[i] in oldToNewTempId:
                            s.exp.items[i] = oldToNewTempId[s.exp.items[i]]
                if isinstance(s, CallStmt):
                    for i in range(len(s.callExp.args)):
                        if s.callExp.args[i] in oldToNewTempId:
                            s.callExp.args[i] = oldToNewTempId[s.callExp.args[i]]
                if isinstance(s, IfStmt):
                    for i in range(len(s.relExp.items)):
                        if s.relExp.items[i] in oldToNewTempId:
                            s.relExp.items[i] = oldToNewTempId[s.relExp.items[i]]






    ################################################################################################

    # IR3 Generation Logic

    ################################################################################################

    def genProgram(self):
        cDataList = self.genCDataList(self.ast.root)
        cMtdList = self.genCMtdList(self.ast.root)
        self.program = Program(cDataList, cMtdList)

    def genCDataList(self, programNode:ProgramNode):
        cDataList = []
        # Main Class
        cData = CData(programNode.mainClass.cname)
        for field in programNode.mainClass.fields:
            cData.addVarDecl(field.type, field.id)
        cDataList.append(cData)
        self.nextMtdId[cData.cname] = 0
        
        # Other classes
        for c in programNode.classes:
            cData = CData(c.cname)
            for field in c.fields:
                cData.addVarDecl(field.type, field.id)
            cDataList.append(cData)
            self.nextMtdId[cData.cname] = 0
        
        return cDataList


    def genCMtdList(self, programNode:ProgramNode):
        cMtdList = []
        for m in programNode.mainClass.methods:
            mainCname = programNode.mainClass.cname
            newTempId = f'{mainCname}_{self.nextMtdId[mainCname]}'
            self.nextMtdId[mainCname] += 1
            self.storeMethodId(mainCname, m.id, m.formals, newTempId)
        for c in programNode.classes:
            for m in c.methods:
                newTempId = f'{c.cname}_{self.nextMtdId[c.cname]}'
                self.nextMtdId[c.cname] += 1
                self.storeMethodId(c.cname, m.id, m.formals, newTempId)

        for m in programNode.mainClass.methods:
            cMtd = self.genCMtd(programNode.mainClass.cname, m)
            cMtdList.append(cMtd)
        for c in programNode.classes:
            for m in c.methods:
                cMtd = self.genCMtd(c.cname, m)
                cMtdList.append(cMtd)

        return cMtdList

    def genCMtd(self, cname:str, m:MethodNode):
        newTempId = self.getMethodIdByFormals(cname, m.id, m.formals)

        cMtd = CMtd(newTempId, m.retType)
        cMtd.addFormal(cname, "this")
        for f in m.formals:
            cMtd.addFormal(f.type, f.id)
        
        mdBody = self.genMdBody(m, cname)
        cMtd.setMdBody(mdBody)
        return cMtd

    def genMdBody(self, m:MethodNode, cname:str):
        attr = {}
        attr["cname"] = cname
        attr['localVars'] = set()
        attr['localVars'].add('this')
        for f in m.formals:
            attr['localVars'].add(f.id)
        
        mdBody = MdBody()
        for a in m.actuals:
            mdBody.addVarDecl(a.type, a.id)
            attr['localVars'].add(a.id)
        
        # # Assign a temp variable for return expression
        # if m.retType != TYPE_VOID:
        #     id = f'_ret0'
        #     attr['localVars'].add(id, m.retType)

        stmtList = self.genStmtsFromBlock(m.stmts, attr)
        mdBody.stmts = stmtList
        return mdBody
        
    
    def genStmtsFromBlock(self, stmts:'list[StmtNode]', attr:dict):
        stmtList = []
        for i in range(len(stmts)):
            s = stmts[i]
            stmtAttr = copy.deepcopy(attr)
            stmtList += self.genStmtsFromStmt(s, stmtAttr)
        return stmtList

    ################################################################################################

    # IR3 Stmts from Stmt

    ################################################################################################

    def genStmtsFromStmt(self, s:StmtNode, attr:dict):
        stmtList = []
        if isinstance(s, StmtIfNode):
            stmtList += self.genStmtsFromIfStmt(s, attr)
        elif isinstance(s, StmtWhileNode):
            stmtList += self.genStmtsFromWhileStmt(s, attr)
        elif isinstance(s, StmtPrintNode):
            stmtList += self.genStmtsFromPrintStmt(s, attr)
        elif isinstance(s, StmtReadNode):
            stmtList += self.genStmtsFromReadStmt(s, attr)
        elif isinstance(s, StmtVarAssignNode):
            stmtList += self.genStmtsFromVarAssignStmt(s, attr)
        elif isinstance(s, StmtFieldAssignNode):
            stmtList += self.genStmtsFromFieldAssignStmt(s, attr)
        elif isinstance(s, StmtLocalCallNode):
            stmtList += self.genStmtsFromLocalCallStmt(s, attr)
        elif isinstance(s, StmtGlobalCallNode):
            stmtList += self.genStmtsFromGlobalCallStmt(s, attr)
        elif isinstance(s, StmtReturnNode):
            stmtList += self.genStmtsFromReturnStmt(s, attr)
        else:
            print("ir3 error: invalid stmt node")
        return stmtList

    def genStmtsFromIfStmt(self, s:StmtIfNode, attr:dict):

        stmtAttr = copy.deepcopy(attr)
        stmtAttr['b.true'] = self.nextLabel()
        stmtAttr['b.false'] = self.nextLabel()
        stmtAttr['s.next'] = self.nextLabel()
        bStmts = self.genStmtsFromBoolOrExp(s.ifCondExp, stmtAttr)
        s1Stmts = self.genStmtsFromBlock(s.thenStmts, copy.deepcopy(attr))
        s2Stmts = self.genStmtsFromBlock(s.elseStmts, copy.deepcopy(attr))

        stmtList = []
        stmtList += bStmts
        stmtList += [LabelStmt(stmtAttr['b.true'])]
        stmtList += s1Stmts
        stmtList += [GotoStmt(stmtAttr['s.next'])]
        stmtList += [LabelStmt(stmtAttr['b.false'])]
        stmtList += s2Stmts
        stmtList += [LabelStmt(stmtAttr['s.next'])]
        return stmtList

    def genStmtsFromWhileStmt(self, s:StmtWhileNode, attr:dict):
        stmtAttr = copy.deepcopy(attr)
        stmtAttr['s.begin'] = self.nextLabel()
        stmtAttr['b.true'] = self.nextLabel()
        stmtAttr['b.false'] = self.nextLabel()
        stmtAttr['s.next'] = stmtAttr['b.false']
        bStmts = self.genStmtsFromBoolOrExp(s.whileCondExp, stmtAttr)
        s1Stmts = self.genStmtsFromBlock(s.stmts, copy.deepcopy(attr))

        stmtList = []
        stmtList += [LabelStmt(stmtAttr['s.begin'])]
        stmtList += bStmts
        stmtList += [LabelStmt(stmtAttr['b.true'])]
        stmtList += s1Stmts
        stmtList += [GotoStmt(stmtAttr['s.begin'])]
        stmtList += [LabelStmt(stmtAttr['s.next'])]
        return stmtList

    def genStmtsFromPrintStmt(self, s:StmtPrintNode, attr:dict):
        stmtAttr = copy.deepcopy(attr)
        e1Stmts, e1Addr = self.genStmtsFromExp(s.exp, stmtAttr)
        stmtList = []
        stmtList += e1Stmts
        stmtList += [PrintStmt(e1Addr)]
        return stmtList

    def genStmtsFromReadStmt(self, s:StmtReadNode, attr:dict):
        stmtAttr = copy.deepcopy(attr)
        stmtList = []
        stmtList += [ReadStmt(s.id)]
        return stmtList
    
    def genStmtsFromVarAssignStmt(self, s:StmtVarAssignNode, attr:dict):
        stmtAttr = copy.deepcopy(attr)
        e1Stmts, e1Addr = self.genStmtsFromExp(s.resultExp, stmtAttr)
        stmtList = []
        stmtList += e1Stmts
        if s.varId in attr['localVars']:
            stmtList += [AssignIdStmt(s.varId, Exp(e1Addr))]
        else: #TODO: Need to review field assignment (how to update value AT THE ADDRESS)
            e0 = self.nextTempId()
            stmtList += [AssignTypeIdStmt(s.resultExp.type, e0, Exp("this", ".", s.varId))]
            stmtList += [AssignIdStmt(e0, Exp(e1Addr))]
        return stmtList

    def genStmtsFromFieldAssignStmt(self, s:StmtFieldAssignNode, attr:dict):
        stmtAttr = copy.deepcopy(attr)
        e1Stmts, e1Addr = self.genStmtsFromExp(s.classExp, stmtAttr)
        e2Stmts, e2Addr = self.genStmtsFromExp(s.resultExp, stmtAttr)
        stmtList = []
        stmtList += e1Stmts
        stmtList += e2Stmts
        #TODO: Need to review field assignment (how to update value AT THE ADDRESS)
        stmtList += [AssignFieldStmt(e1Addr, s.fieldId, Exp(e2Addr))]
        return stmtList

    def genStmtsFromLocalCallStmt(self, s:StmtLocalCallNode, attr:dict):
        stmtAttr = copy.deepcopy(attr)
        stmtList = []

        argList = ["this"]
        argTypeList = [attr["cname"]]
        # Process arg expression
        for a in s.args:
            stmts, addr = self.genStmtsFromExp(a, stmtAttr)
            stmtList += stmts
            argList += [addr]
            argTypeList += [a.type]
        argTypes = tuple(argTypeList)
        
        methodId = self.getMethodId(attr["cname"], s.methodId, argTypes)
        stmt = CallStmt(CallExp(methodId, argList))
        stmtList += [stmt]
        return stmtList

    def genStmtsFromGlobalCallStmt(self, s:StmtGlobalCallNode, attr:dict):
        stmtAttr = copy.deepcopy(attr)
        stmtList = []
        stmts, e1 = self.genStmtsFromExp(s.classExp, stmtAttr)
        stmtList += stmts
        argList = [e1]
        argTypeList = [s.classExp.type]
        # Process arg expression
        for a in s.args:
            stmts, addr = self.genStmtsFromExp(a, stmtAttr)
            stmtList += stmts
            argList += [addr]
            argTypeList += [a.type]
        argTypes = tuple(argTypeList)
        methodId = self.getMethodId(s.classExp.type, s.methodId, argTypes)
        stmt = CallStmt(CallExp(methodId, argList))
        stmtList += [stmt]
        return stmtList

    def genStmtsFromReturnStmt(self, s:StmtReturnNode, attr:dict):
        stmtAttr = copy.deepcopy(attr)
        stmtList = []
        if s.isVoid:
            stmtList += [ReturnStmt("")]
        else:
            stmts, e1 = self.genStmtsFromExp(s.returnExp, stmtAttr)
            stmtList += stmts
            stmtList += [ReturnStmt(e1)]
        return stmtList

    ################################################################################################

    # IR3 Stmts from Exp

    ################################################################################################


    def genStmtsFromExp(self, e:ExpNode, attr:dict) -> 'tuple[list[Stmt], str]':
        stmtList = []
        expAttr = copy.deepcopy(attr)
        if isinstance(e, ExpBoolOrNode):
            e0 = self.nextTempId()
            expAttr['b.true'] = self.nextLabel()
            expAttr['b.false'] = self.nextLabel()
            expAttr['b.next'] = self.nextLabel()
            bStmts = self.genStmtsFromBoolOrExp(e, expAttr)
            s1Stmts = [AssignTypeIdStmt(e.type, e0, Exp("true"))] 
            s2Stmts = [AssignIdStmt(e0, Exp("false"))]
            
            stmtList += s1Stmts 
            stmtList += bStmts
            stmtList += [LabelStmt(expAttr['b.true'])]
            # # Do nothing since e0 = true already
            stmtList += [GotoStmt(expAttr['b.next'])]
            stmtList += [LabelStmt(expAttr['b.false'])]
            stmtList += s2Stmts
            stmtList += [LabelStmt(expAttr['b.next'])]
            return stmtList, e0

        if isinstance(e, ExpAddNode) or \
           isinstance(e, ExpSubNode) or \
           isinstance(e, ExpMulNode) or \
           isinstance(e, ExpDivNode):
            if e.category == EXP_ADD: op = "+"
            if e.category == EXP_SUB: op = "-"
            if e.category == EXP_MUL: op = "*"
            if e.category == EXP_DIV: op = "/"

            e1Stmts, e1Addr = self.genStmtsFromExp(e.firstExp, expAttr)
            e2Stmts, e2Addr = self.genStmtsFromExp(e.secondExp, expAttr)
            if re.match(r"[0-9]+", e1Addr) is not None or re.match(r"\".*\"", e1Addr) is not None:
                e0 = self.nextTempId()
                stmt = AssignTypeIdStmt(e.type, e0, Exp(str(e1Addr), op, e2Addr))
                e1Addr = e0
            else:
                stmt = AssignIdStmt(e1Addr, Exp(e1Addr, op, e2Addr))
            stmtList += e1Stmts
            stmtList += e2Stmts
            stmtList += [stmt]
            return stmtList, e1Addr

        if isinstance(e, ExpIntBaseNode):
            e1Stmts, e1Addr = self.genStmtsFromExp(e.exp, expAttr)
            stmtList += e1Stmts
            if e.isNegated:
                if re.match(r"[0-9]+", e1Addr) is not None:
                    e0 = self.nextTempId()
                    stmt = AssignTypeIdStmt(e.type, e0, Exp("-", str(e1Addr)))
                    e1Addr = e0
                else:
                    stmt = AssignIdStmt(e1Addr, Exp("-", e1Addr))
                stmtList += [stmt]
            return stmtList, e1Addr

        if isinstance(e, ExpIntNode):
            return stmtList, e.val

        if isinstance(e, ExpStringNode):
            return stmtList, e.val

        if isinstance(e, ExpVarNode):
            if e.varId in attr['localVars']:
                return stmtList, e.varId
            else:
                e0 = self.nextTempId()
                stmt = AssignTypeIdStmt(e.type, e0, Exp("this", ".", e.varId))
                stmtList += [stmt]
                return stmtList, e0

        if isinstance(e, ExpFieldNode):
            e0 = self.nextTempId()
            e1Stmts, e1Addr = self.genStmtsFromExp(e.classExp, expAttr)
            stmt = AssignTypeIdStmt(e.type, e0, Exp(e1Addr, ".", e.fieldId))
            stmtList += e1Stmts
            stmtList += [stmt]
            return stmtList, e0

        if isinstance(e, ExpLocalCallNode):
            argList = ["this"]
            argTypeList = [attr['cname']]
            # Process arg expression
            for a in e.args:
                stmts, addr = self.genStmtsFromExp(a, expAttr)
                stmtList += stmts
                argList += [addr]
                argTypeList += [a.type]
            argTypes = tuple(argTypeList)
            methodId = self.getMethodId(attr["cname"], e.methodId, argTypes)
            e0 = self.nextTempId()
            stmt = AssignTypeIdStmt(e.type, e0, CallExp(methodId, argList))
            stmtList += [stmt]
            return stmtList, e0
        
        if isinstance(e, ExpGlobalCallNode):
            # Process class expression
            stmts, e1 = self.genStmtsFromExp(e.classExp, expAttr)
            stmtList += stmts
            argList = [e1]
            argTypeList = [e.classExp.type]
            # Process arg expression
            for a in e.args:
                stmts, addr = self.genStmtsFromExp(a, expAttr)
                stmtList += stmts
                argList += [addr]
                argTypeList += [a.type]
            argTypes = tuple(argTypeList)
            methodId = self.getMethodId(e.classExp.type, e.methodId, argTypes)
            e0 = self.nextTempId()
            stmt = AssignTypeIdStmt(e.type, e0, CallExp(methodId, argList))
            stmtList += [stmt]
            return stmtList, e0

        if isinstance(e, ExpNewClassNode):
            e0 = self.nextTempId()
            stmt = AssignTypeIdStmt(e.type, e0, Exp("new", e.type, "()"))
            stmtList += [stmt]
            return stmtList, e0
            
        if isinstance(e, ExpNullNode):
            return stmtList, "NULL"


    def genStmtsFromBoolOrExp(self, b:ExpBoolOrNode, attr:dict):
        stmtList = []
        for i in range(len(b.andExps)):
            exprAttr = copy.deepcopy(attr)
            exprAttr['b1.true'] = attr['b.true']
            exprAttr['b1.false'] = self.nextLabel()
            b1Stmts = self.genStmtsFromBoolAndExp(b.andExps[i], exprAttr)
            stmtList += b1Stmts
            stmtList += [LabelStmt(exprAttr['b1.false'])]
        stmtList += [GotoStmt(exprAttr['b.false'])]
        return stmtList

    def genStmtsFromBoolAndExp(self, b:ExpBoolAndNode, attr:dict):
        stmtList = []
        for i in range(len(b.relExps)):
            exprAttr = copy.deepcopy(attr)
            exprAttr['b2.false'] = attr['b1.false'] # short circuit from (False && ???) to check next item in OR chain
            exprAttr['b2.true'] = self.nextLabel()
            b2Stmts = self.genStmtsFromBoolRelExp(b.relExps[i], exprAttr)
            stmtList += b2Stmts
            stmtList += [LabelStmt(exprAttr['b2.true'])]
        stmtList += [GotoStmt(attr['b1.true'])] # passes whole of (? && ? && ...), goto true of OR chain
        return stmtList

    def genStmtsFromBoolRelExp(self, b:TNode, attr:dict):
        stmtList = []
        exprAttr = copy.deepcopy(attr)

        if isinstance(b, ExpBoolRelNode):
            exprAttr['b3.true'] = exprAttr['b2.true']
            exprAttr['b3.false'] = exprAttr['b2.false']
            
            e1Stmts, e1Addr = self.genStmtsFromExp(b.firstExp, attr)
            e2Stmts, e2Addr = self.genStmtsFromExp(b.secondExp, attr)
            ifStmt = IfStmt()
            ifStmt.labelNum = exprAttr['b3.true']
            ifStmt.relExp = RelExp(e1Addr, b.op, e2Addr)
            stmtList += e1Stmts
            stmtList += e2Stmts
            stmtList += [ifStmt]
            stmtList += [GotoStmt(exprAttr['b3.false'])]

        elif isinstance(b, ExpBoolBaseNode):
            # Swap true and false label if negated
            if b.isNegated:
                exprAttr['b3.true'] = exprAttr['b2.false']
                exprAttr['b3.false'] = exprAttr['b2.true']
            else:
                exprAttr['b3.true'] = exprAttr['b2.true']
                exprAttr['b3.false'] = exprAttr['b2.false']
            
            if isinstance(b.exp, ExpBoolNode):
                if b.exp.val == "true":
                    stmtList += [GotoStmt(exprAttr['b3.true'])]
                elif b.exp.val == "false":
                    stmtList += [GotoStmt(exprAttr['b3.false'])]
                else:
                    print("ir3 error: value of ExpBoolNode not set")
            else:
                e1Stmts, e1Addr = self.genStmtsFromExp(b.exp, exprAttr)
                ifStmt = IfStmt()
                ifStmt.labelNum = exprAttr['b3.true']
                ifStmt.relExp = RelExp(e1Addr)
                stmtList += e1Stmts
                stmtList += [ifStmt]
                stmtList += [GotoStmt(exprAttr['b3.false'])]
                
        else:
            print("ir3 error: Unexpected tree node while processing Bool Rel Exp")

        return stmtList



if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Usage: python ir3.py filename")
        print("Usage: ./ir3.py filename")
        exit(1)

    filename = sys.argv[1]
    try:
        f = open(filename)
    except FileNotFoundError as e:
        print(e)
        exit(1)

    if len(sys.argv) > 2:
        debug = int(sys.argv[2])

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
