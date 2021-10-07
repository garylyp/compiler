#!/usr/bin/env python

import sys
from parse import PNode, Parser

# Node types
PROGRAM = "Program"
CLASS = "Class"
VARIABLE = "Variable"
METHOD = "Method"
STMT = "Stmt"
EXP = "Exp"

# Stmt types
STMT_IF = "StmtIf"
STMT_WHILE = "StmtWhile"
STMT_PRINT = "StmtPrint"
STMT_READ = "StmtRead"
STMT_VAR_ASSIGN = "StmtVarAssign"
STMT_FIELD_ASSIGN = "StmtFieldAssign"
STMT_LOCAL_CALL = "StmtLocalCall"
STMT_GLOBAL_CALL = "StmtGlobalCall"
STMT_RETURN = "StmtReturn"
STMT_RETURN_VOID = "StmtReturnVoid"

# Exp types
EXP_BOOL_OR = "ExpBoolOr"   # x || y || false
EXP_BOOL_AND = "ExpBoolAnd" # x && y && true 
EXP_BOOL_REL = "ExpBoolRel" # > < >= <= != ==
EXP_BOOL_BASE = "ExpBoolBase"           # /  !!true   /   !false    / !ExpField / !ExpLocalCall / !ExpGlobalCall
EXP_BOOL = "ExpBool" # true, false

EXP_ADD  = "ExpAdd"
EXP_SUB  = "ExpSub"
EXP_MUL  = "ExpMul"
EXP_DIV  = "ExpDiv"
EXP_INT_BASE = "ExpIntBase"   # ----1 / 1 / -ExpField / -ExpLocalCall / -ExpGlobalCall
EXP_INT = "ExpInt"

EXP_STRING = "ExpString"

EXP_VAR = "ExpVar"                   # id
EXP_FIELD = "ExpField"               # m.id
EXP_LOCAL_CALL = "ExpLocalCall"      # id ( ExpList )
EXP_GLOBAL_CALL = "ExpGlobalCall"    # m.id ( ExpList )
EXP_NEW_CLASS = "ExpNewClass"        # new Object()
EXP_NULL = "ExpNull"                 # null


# Stmt / Exp Types
TYPE_INT = "Int"
TYPE_BOOL = "Bool"
TYPE_STRING = "String"
TYPE_VOID = "Void"

def errorF(msg):
    print(msg)
    exit(1)

################################################################################################

# AST Nodes

################################################################################################


class TNode:
    def __init__(self, entity:str):
        """
        entity : a string specifying the type of this AST node
        """
        self.entity = entity
        self.attr = {}

class ProgramNode(TNode):
    classes:'list[ClassNode]'
    mainClass:'ClassNode'

    def __init__(self):
        super().__init__(PROGRAM)
        self.mainClass = None
        self.classes = []
    
    def setMainClass(self, classNode:'ClassNode'):
        self.mainClass = classNode

    def addClass(self, classNode:'ClassNode'):
        self.classes.append(classNode)

class ClassNode(TNode):
    fields:'list[VariableNode]'
    methods:'list[MethodNode]'

    def __init__(self):
        super().__init__(CLASS)
        self.fields = []
        self.methods = []

    def setCname(self, cname):
        self.cname = cname

    def addField(self, variableNode):
        self.fields.append(variableNode)

    def addMethod(self, methodNode):
        self.methods.append(methodNode)

class VariableNode(TNode):
    def __init__(self, id:str, type:str):
        super().__init__(VARIABLE)
        self.id = id
        self.type = type

class MethodNode(TNode):
    formals:'list[VariableNode]'
    actuals:'list[VariableNode]'
    stmts:'list[StmtNode]'

    def __init__(self, id:str, retType:str):
        super().__init__(METHOD)
        self.id = id
        self.retType = retType
        self.formals = []
        self.actuals = []
        self.stmts = []

    def addFormal(self, variableNode):
        self.formals.append(variableNode)

    def addActual(self, variableNode):
        self.actuals.append(variableNode)

    def addStmt(self, stmtNode):
        self.stmts.append(stmtNode)

################################################################################################

# STATEMENT

################################################################################################

class StmtNode(TNode):
    def __init__(self, category):
        super().__init__(STMT)
        self.category = category
        self.type = None

    def setType(self, type):
        self.type = type

class StmtIfNode(StmtNode):
    def __init__(self):
        super().__init__(STMT_IF)
        self.ifCondExp = None
        self.thenStmts = []
        self.elseStmts = []

    def setIfCondExp(self, expNode):
        self.ifCondExp = expNode

    def addThenStmt(self, stmtNode):
        self.thenStmts.append(stmtNode)

    def addElseStmt(self, stmtNode):
        self.elseStmts.append(stmtNode)

class StmtWhileNode(StmtNode):
    def __init__(self):
        super().__init__(STMT_WHILE)
        self.whileCondExp = None
        self.stmts = []

    def setWhileCondExp(self, expNode):
        self.whileCondExp = expNode

    def addStmt(self, stmtNode):
        self.stmts.append(stmtNode)

class StmtReadNode(StmtNode):
    def __init__(self):
        super().__init__(STMT_READ)
        
    def setId(self, id):
        self.id = id

class StmtPrintNode(StmtNode):
    def __init__(self):
        super().__init__(STMT_PRINT)
    
    def setExp(self, expNode):
        self.exp = expNode

class StmtVarAssignNode(StmtNode):
    def __init__(self):
        super().__init__(STMT_VAR_ASSIGN)

    def setVarId(self, varId):
        self.varId = varId

    def setResultExp(self, expNode):
        self.resultExp = expNode

class StmtFieldAssignNode(StmtNode):
    def __init__(self):
        super().__init__(STMT_FIELD_ASSIGN)
    
    def setClassExp(self, expNode):
        self.classExp = expNode

    def setFieldId(self, fieldId):
        self.fieldId = fieldId

    def setResultExp(self, expNode):
        self.resultExp = expNode

class StmtLocalCallNode(StmtNode):
    def __init__(self):
        super().__init__(STMT_LOCAL_CALL)
        self.args = []
        
    def setMethodId(self, methodId):
        self.methodId = methodId

    def addArgExp(self, expNode):
        self.args.append(expNode)

class StmtGlobalCallNode(StmtNode):
    def __init__(self):
        super().__init__(STMT_GLOBAL_CALL)
        self.args = []

    def setClassExp(self, expNode):
        self.classExp = expNode
        
    def setMethodId(self, methodId):
        self.methodId = methodId

    def addArgExp(self, expNode):
        self.args.append(expNode)

class StmtReturnNode(StmtNode):
    def __init__(self):
        super().__init__(STMT_RETURN)
        self.isVoid = False
    
    def setVoid(self, isVoid):
        self.isVoid = isVoid

    def setReturnExp(self, expNode):
        self.returnExp = expNode

################################################################################################

# Exp Nodes (BOOL)

################################################################################################

class ExpNode(TNode):
    def __init__(self, category):
        super().__init__(EXP)
        self.category = category

    def setType(self, type):
        self.type = type

class ExpBoolOrNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_BOOL_OR)
        self.andExps = []

    def addAndExp(self, expNode):
        self.andExps.append(expNode)
    
class ExpBoolAndNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_BOOL_AND)
        self.relExps = []

    def addRelExp(self, expNode):
        self.relExps.append(expNode)

class ExpBoolRelNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_BOOL_REL)

    def setFirstExp(self, expNode):
        self.firstExp = expNode

    def setSecondExp(self, expNode):
        self.secondExp = expNode

    def setOp(self, op):
        self.op = op

class ExpBoolBaseNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_BOOL_BASE)
        self.isNegated = False
    
    def setNegated(self, isNegated):
        self.isNegated = isNegated

    def setExp(self, expNode):
        self.exp = expNode

class ExpBoolNode(ExpNode):
    def __init__(self, val):
        super().__init__(EXP_BOOL)
        super().setType(TYPE_BOOL)
        self.val = val

################################################################################################

# Exp Nodes (INT)

################################################################################################

class ExpAddNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_ADD)

    def setFirstExp(self, expNode):
        self.setFirstExp = expNode

    def setSecondExp(self, expNode):
        self.secondExp = expNode

class ExpSubNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_SUB)

    def setFirstExp(self, expNode):
        self.setFirstExp = expNode

    def setSecondExp(self, expNode):
        self.secondExp = expNode

class ExpMulNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_MUL)

    def setFirstExp(self, expNode):
        self.setFirstExp = expNode

    def setSecondExp(self, expNode):
        self.secondExp = expNode

class ExpDivNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_DIV)

    def setFirstExp(self, expNode):
        self.setFirstExp = expNode

    def setSecondExp(self, expNode):
        self.secondExp = expNode

class ExpIntBaseNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_INT_BASE)
        self.isNegated = False
    
    def setNegated(self, isNegated):
        self.isNegated = isNegated

    def setExp(self, expNode):
        self.exp = expNode

class ExpIntNode(ExpNode):
    def __init__(self, val):
        super().__init__(EXP_INT)
        super().setType(TYPE_INT)
        self.val = val

################################################################################################

# Exp Nodes (String)

################################################################################################

class ExpStringNode(ExpNode):
    def __init__(self, val):
        super().__init__(EXP_STRING)
        self.val = val

################################################################################################

# Exp Atoms 

################################################################################################

class ExpVarNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_VAR)

    def setVarId(self, varId):
        self.varId = varId


class ExpFieldNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_FIELD)

    def setClassExp(self, expNode):
        self.classExp = expNode

    def setFieldId(self, fieldId):
        self.fieldId = fieldId

class ExpLocalCallNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_LOCAL_CALL)
        self.args = []

    def setMethodId(self, methodId):
        self.methodId = methodId

    def addArgExp(self, expNode):
        self.args.append(expNode)

class ExpGlobalCallNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_GLOBAL_CALL)
        self.args = []

    def setClassExp(self, expNode):
        self.classExp = expNode
        
    def setMethodId(self, methodId):
        self.methodId = methodId

    def addArgExp(self, expNode):
        self.args.append(expNode)

class ExpNewClassNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_NEW_CLASS)

class ExpNullNode(ExpNode):
    def __init__(self):
        super().__init__(EXP_NULL)

################################################################################################

# AST

################################################################################################


class AST:
    def __init__(self, parseTree:PNode):
        self.root = self.constructAST(parseTree)

    def validate(self, expected, actual):
        if isinstance(actual, PNode):
            actual = actual.value
        if expected == actual:
            return
        raise Exception(f'Expected {expected} node but got {actual}')
        

    def constructAST(self, pNode:PNode):
        self.validate("Program", pNode)
        node = self.genProgram(pNode)
        return node

    def genProgram(self, pNode:PNode):
        tNode = ProgramNode()
        mainClassNode = self.genMainClass(pNode.children[0])
        tNode.setMainClass(mainClassNode)
        for i in range(1, len(pNode.children)):
            self.validate("ClassDecl", pNode.children[i])
            classNode = self.genClass(pNode.children[i])
            tNode.addClass(classNode)
        return tNode

    def genMainClass(self, pNode:PNode):
        tNode = ClassNode()
        self.validate("Cname", pNode.children[1])
        cname = self.genCname(pNode.children[1])
        tNode.setCname(cname)

        self.validate("Void", pNode.children[3])
        self.validate("main", pNode.children[4])

        mainMethodNode = MethodNode("main", "Void")
        i = 6
        while isinstance(pNode.children[i], PNode) and pNode.children[i].value == "Fml":
            varNode = self.genVar(pNode.children[i])
            mainMethodNode.addFormal(varNode)
            i += 2
        
        if isinstance(pNode.children[i], str) and pNode.children[i] == ")":
            i += 1

        self.validate("MdBody", pNode.children[i])
        mdBodyNode = pNode.children[i]
        i = 1 # i = 0 is the '{'
        while isinstance(mdBodyNode.children[i], PNode) and mdBodyNode.children[i].value == "VarDecl":
            varNode = self.genVar(mdBodyNode.children[i])
            mainMethodNode.addActual(varNode)
            i += 1

        while isinstance(mdBodyNode.children[i], PNode) and mdBodyNode.children[i].value == "Stmt":
            stmtNode = self.genStmt(mdBodyNode.children[i])
            mainMethodNode.addStmt(stmtNode)
            i += 1

        tNode.addMethod(mainMethodNode)
        return tNode

    def genClass(self, pNode:PNode):
        tNode = ClassNode()
        self.validate("Cname", pNode.children[1])
        cname = self.genCname(pNode.children[1])
        tNode.setCname(cname)

        i = 3
        while isinstance(pNode.children[i], PNode) and pNode.children[i].value == "VarDecl":
            varNode = self.genVar(pNode.children[i])
            tNode.addField(varNode)
            i += 1

        while isinstance(pNode.children[i], PNode) and pNode.children[i].value == "MdDecl":
            methodNode = self.genMethod(pNode.children[i])
            tNode.addMethod(methodNode)
            i += 1

        return tNode
            
    def genMethod(self, pNode:PNode):
        self.validate("MdDecl", pNode)
        self.validate("Type", pNode.children[0])
        self.validate("Id", pNode.children[1])
        methodType = self.genType(pNode.children[0])
        methodId = self.genId(pNode.children[1])
        tNode = MethodNode(methodId, methodType)
        i = 3
        while isinstance(pNode.children[i], PNode) and pNode.children[i].value == "Fml":
            varNode = self.genVar(pNode.children[i])
            tNode.addFormal(varNode)
            i += 2

        mdBodyNode = pNode.children[i]
        i = 1 # i = 0 is the '{'
        while isinstance(mdBodyNode.children[i], PNode) and mdBodyNode.children[i].value == "VarDecl":
            varNode = self.genVar(mdBodyNode.children[i])
            tNode.addActual(varNode)
            i += 1

        while isinstance(mdBodyNode.children[i], PNode) and mdBodyNode.children[i].value == "Stmt":
            stmtNode = self.genStmt(mdBodyNode.children[i])
            tNode.addStmt(stmtNode)
            i += 1

        return tNode


    def genType(self, pNode:PNode) -> str:
        self.validate("Type", pNode)
        if isinstance(pNode.children[0], PNode):
            self.validate("Cname", pNode.children[0])
            typeVal = pNode.children[0].children[0]
            return typeVal.lower().capitalize()
        else:
            return pNode.children[0].lower().capitalize()

    def genId(self, pNode:PNode) -> str:
        self.validate("Id", pNode)
        return pNode.children[0].lower()

    def genCname(self, pNode:PNode) -> str:
        self.validate("Cname", pNode)
        return pNode.children[0].lower().capitalize()

    def genVar(self, pNode:PNode):
        self.validate("Type", pNode.children[0])
        self.validate("Id", pNode.children[1])
        varType = self.genType(pNode.children[0])
        varId = self.genId(pNode.children[1])
        varNode = VariableNode(varId, varType)
        return varNode

    def genStmt(self, pNode:PNode):
        self.validate("Stmt", pNode)
        if pNode.children[0].value == "StmtIf":
            return self.genIfStmt(pNode.children[0])
        elif pNode.children[0].value == "StmtWhile":
            return self.genWhileStmt(pNode.children[0])
        elif pNode.children[0].value == "StmtReadln":
            return self.genReadStmt(pNode.children[0])
        elif pNode.children[0].value == "StmtPrintln":
            return self.genPrintStmt(pNode.children[0])
        elif pNode.children[0].value == "StmtReturn":
            return self.genReturnStmt(pNode.children[0])
        elif pNode.children[0].value == "StmtAssign":
            return self.genAssignStmt(pNode.children[0])
        elif pNode.children[0].value == "Atom":
            return self.genCallStmt(pNode.children[0])
        else:
            self.validate("Stmt", "invalid_stmt_type")


    def genIfStmt(self, pNode:PNode):
        self.validate("StmtIf", pNode)
        tNode = StmtIfNode()
        self.validate("Exp", pNode.children[2])
        self.validate("BoolExp", pNode.children[2].children[0])
        ifCondExpNode = self.genBoolExp(pNode.children[2].children[0])
        tNode.setIfCondExp(ifCondExpNode)

        i = 5
        while isinstance(pNode.children[i], PNode) and pNode.children[i].value == "Stmt":
            stmtNode = self.genStmt(pNode.children[i])
            tNode.addThenStmt(stmtNode)
            i += 1
        
        i = i + 3
        while isinstance(pNode.children[i], PNode) and pNode.children[i].value == "Stmt":
            stmtNode = self.genStmt(pNode.children[i])
            tNode.addElseStmt(stmtNode)
            i += 1

        return tNode

    def genWhileStmt(self, pNode:PNode):
        self.validate("StmtWhile", pNode)
        tNode = StmtWhileNode()
        self.validate("Exp", pNode.children[2])
        self.validate("BoolExp", pNode.children[2].children[0])
        whileCondExpNode = self.genBoolExp(pNode.children[2].children[0])
        tNode.setWhileCondExp(whileCondExpNode)

        i = 5
        while isinstance(pNode.children[i], PNode) and pNode.children[i].value == "Stmt":
            stmtNode = self.genStmt(pNode.children[i])
            tNode.addStmt(stmtNode)
            i += 1

        return tNode

    def genReadStmt(self, pNode:PNode):
        self.validate("StmtReadln", pNode)
        tNode = StmtReadNode()
        self.validate("Id", pNode.children[2])
        id = self.genId(pNode.children[2])
        tNode.setId(id)
        return tNode


    def genPrintStmt(self, pNode:PNode):
        self.validate("StmtPrintln", pNode)
        tNode = StmtPrintNode()
        self.validate("Exp", pNode.children[2])
        expNode = self.genExp(pNode.children[2])
        tNode.setExp(expNode)
        return tNode

    def genReturnStmt(self, pNode:PNode):
        self.validate("StmtReturn", pNode)
        tNode = StmtReturnNode()
        if isinstance(pNode.children[1], str) and pNode.children[1] == ";":
            tNode.setVoid(True)
        else:
            self.validate("Exp", pNode.children[1])
            expNode = self.genExp(pNode.children[1])
            tNode.setReturnExp(expNode)
            tNode.setVoid(False)
        return tNode

    def genAssignStmt(self, pNode:PNode):
        self.validate("StmtAssign", pNode)
        
        if isinstance(pNode.children[0], PNode) and pNode.children[0].value == "Id":
            tNode = StmtVarAssignNode()
            self.validate("Exp", pNode.children[2])
            id = self.genId(pNode.children[0])
            exp = self.genExp(pNode.children[2])
            tNode.setVarId(id)
            tNode.setResultExp(exp)
            return tNode
    

        self.validate("Atom", pNode.children[0])
        tNode = StmtFieldAssignNode()
        atom = pNode.children[0]
        classExp = self.genClassExp(atom.children[:-2])
        tNode.setClassExp(classExp)

        self.validate("Id", atom.children[-1])
        id = self.genId(atom.children[-1])
        tNode.setFieldId(id)

        return tNode


    def genCallStmt(self, pNode:PNode):
        self.validate("Atom", pNode)
        
        if len(pNode.children) == 4:  # id ( ExpList )
            tNode = ExpLocalCallNode()
        else:
            tNode = ExpGlobalCallNode()
            classExp = self.genClassExp(pNode.children[:-5])
            tNode.setClassExp(classExp)
        
        self.validate("Id", pNode.children[-4])
        methodId = self.genId(pNode.children[-4])
        tNode.setMethodId(methodId)
        
        self.validate("ExpList", pNode.children[-2])
        expListNode = pNode.children[-2]
        for c in expListNode.children:
            if isinstance(c, PNode):
                exp = self.genExp(c)
                tNode.addArgExp(exp)
    
        return tNode


    def genExp(self, pNode:PNode):
        self.validate("Exp", pNode)
        if isinstance(pNode.children[0], PNode) and pNode.children[0].value == "BoolExp":
            return self.genBoolExp(pNode.children[0])
        elif isinstance(pNode.children[0], PNode) and pNode.children[0].value == "MathExp":
            return self.genMathExp(pNode.children[0])
        else:
            return self.genStringExp(pNode)

    def genBoolExp(self, pNode:PNode):
        self.validate("BoolExp", pNode)
        tNode = ExpBoolOrNode()
        for c in pNode.children:
            if isinstance(c, PNode):
                self.validate("Conj", c)
                andExpNode = self.genBoolAndExp(c)
                tNode.addAndExp(andExpNode)
        return tNode

    def genBoolAndExp(self, pNode:PNode):
        self.validate("Conj", pNode)
        tNode = ExpBoolAndNode()
        for c in pNode.children:
            if isinstance(c, PNode):
                self.validate("RelExp", c)
                relExpNode = self.genBoolRelExp(c)
                tNode.addRelExp(relExpNode)
        return tNode

    def genBoolRelExp(self, pNode:PNode):
        self.validate("RelExp", pNode.value)
        if isinstance(pNode.children[0], PNode) and pNode.children[0].value == "MathExp":
            self.validate("MathExp", pNode.children[2])
            tNode = ExpBoolRelNode()
            firstExpNode = self.genMathExp(pNode.children[0])
            secondExpNode = self.genMathExp(pNode.children[2])
            tNode.setFirstExp(firstExpNode)
            tNode.setSecondExp(secondExpNode)
            tNode.setOp(pNode.children[1])
            tNode.setType(TYPE_BOOL)
            return tNode
        
        else:
            tNode = self.genBoolBaseExp(pNode)
            return tNode

    def genBoolBaseExp(self, pNode:PNode):
        """
        !!!!true / false / !atom / atom
        """
        self.validate("RelExp", pNode)
        tNode = ExpBoolBaseNode()
        isNeg = False
        i = 0
        while isinstance(pNode.children[i], str) and pNode.children[i] == "!":
            isNeg = not isNeg
            i += 1
        tNode.setNegated(isNeg)
        if isinstance(pNode.children[i], str):
            val = pNode.children[i] # true / false
            expBoolNode = ExpBoolNode(val)
            expBoolNode.setType(TYPE_BOOL)
            tNode.setExp(expBoolNode)
            return tNode
        
        self.validate("Atom", pNode.children[i])
        expNode = self.genClassExp(pNode.children[i].children)
        tNode.setExp(expNode)
        return tNode

    def genMathExp(self, pNode:PNode):
        self.validate("MathExp", pNode)
        i = 0
        tNode = self.genTermExp(pNode.children[i])

        i += 1
        while i < len(pNode.children):
            if pNode.children[i] == "+":
                parent = ExpAddNode()
            elif pNode.children[i] == "-":
                parent = ExpSubNode()
            else:
                self.validate("+ or -", pNode.children[i])
            
            nextNode = self.genTermExp(pNode.children[i+1])
            parent.setFirstExp(tNode)
            parent.setSecondExp(nextNode)
            tNode = parent
            i += 2
        return tNode

    def genTermExp(self, pNode:PNode):
        self.validate("Term", pNode)
        i = 0
        tNode = self.genFactorExp(pNode.children[i])

        i += 1
        while i < len(pNode.children):
            if pNode.children[i] == "*":
                parent = ExpMulNode()
            elif pNode.children[i] == "/":
                parent = ExpDivNode()
            else:
                self.validate("* or /", pNode.children[i])
            
            nextNode = self.genFactorExp(pNode.children[i+1])
            parent.setFirstExp(tNode)
            parent.setSecondExp(nextNode)
            tNode = parent
            i += 2
        return tNode

    def genFactorExp(self, pNode:PNode):
        """
        ---1 / 1 / atom / -atom / + - * /
        """
        self.validate("Factor", pNode)
        tNode = ExpIntBaseNode()
        i = 0
        isNeg = False
        while isinstance(pNode.children[i], str) and pNode.children[i] == "-":
            isNeg = not isNeg
            i += 1
        tNode.setNegated(isNeg)
        if isinstance(pNode.children[i], str):
            val = pNode.children[i] # 112 / 1212 / int
            intNode = ExpIntNode(val)
            tNode.setExp(intNode)
            return tNode

        self.validate("Atom", pNode.children[i])
        expNode = self.genClassExp(pNode.children[i].children)
        tNode.setExp(expNode)
        return tNode
        

    def genClassExp(self, nodes:list):
        """
        where m = Id / 'this' / 'null' / 'new' Cname '(' ')'

        m 
        m . Id
        m . Id ( ExpList )

        m ( ExpList )

        ( Exp )
        ( Exp ) . Id
        ( Exp ) . Id ( ExpList )
        """
        if len(nodes) == 1:
            # m
            if isinstance(nodes[0], PNode):
                self.validate("Id", nodes[0])
                varId = self.genId(nodes[0])
                tNode = ExpVarNode()
                tNode.setVarId(varId)
                return tNode
            elif isinstance(nodes[0], str):
                if nodes[0] == "this":
                    varId = nodes[0]
                    tNode = ExpVarNode()
                    tNode.setVarId(varId)
                    return tNode
                elif nodes[0] == "null":
                    tNode = ExpNullNode()
                    return tNode    

        if len(nodes) == 3 and \
            isinstance(nodes[0], str) and \
            isinstance(nodes[1], PNode) and \
            isinstance(nodes[2], str):
            self.validate("(", nodes[0])
            self.validate("Exp", nodes[1])
            self.validate(")", nodes[2])
            expNode = self.genExp(nodes[1])
            return expNode

        if len(nodes) == 4 and \
            isinstance(nodes[0], str) and \
            isinstance(nodes[1], PNode) and \
            isinstance(nodes[2], str) and \
            isinstance(nodes[3], str):
            self.validate("new", nodes[0])
            self.validate("Cname", nodes[1])
            self.validate("(", nodes[2])
            self.validate(")", nodes[3])
            cname = self.genCname(nodes[1])
            newClassNode = ExpNewClassNode()
            newClassNode.setType(cname)
            return newClassNode

        if len(nodes) >= 4 and \
            isinstance(nodes[-4], PNode) and \
            isinstance(nodes[-3], str) and \
            isinstance(nodes[-2], PNode) and \
            isinstance(nodes[-1], str):
            self.validate("Id", nodes[-4])
            self.validate("(", nodes[-3])
            self.validate("ExpList", nodes[-2])
            self.validate(")", nodes[-1])
            if len(nodes[:-4]) == 0:
                tNode = ExpLocalCallNode()
            else:
                self.validate(".", nodes[-5])
                tNode = ExpGlobalCallNode()
                classExpNode = self.genClassExp(nodes[:-5])
                tNode.setClassExp(classExpNode)

            methodId = self.genId(nodes[0])
            tNode.setMethodId(methodId)

            for c in nodes[2].children:
                if isinstance(c, PNode):
                    exp = self.genExp(c)
                    tNode.addArgExp(exp)
            return tNode
        
        # else len(nodes) >= 2
        if len(nodes) >= 2 and isinstance(nodes[-1], PNode) and isinstance(nodes[-2], str):
            # atom . id
            self.validate("Id", nodes[-1])
            self.validate(".", nodes[-2])
            tNode = ExpFieldNode()
            fieldId = self.genId(nodes[-1])
            classExpNode = self.genClassExp(nodes[:-2])
            tNode.setFieldId(fieldId)
            tNode.setClassExp(classExpNode)
            return tNode


    def genStringExp(self, pNode:PNode):
        """
        Might be a string expression, or a ADD on a sequence of atoms
        """
        self.validate("Exp", pNode)
        i = 0
        if isinstance(pNode.children[i], str):
            tNode = ExpStringNode(pNode.children[i])
        else:
            self.validate("Atom", pNode.children[i])
            tNode = self.genClassExp(pNode.children[i].children)

        i += 1
        while i < len(pNode.children):
            self.validate("+", pNode.children[i])
            parent = ExpAddNode()
            if isinstance(pNode.children[i+1], str):
                nextNode = ExpStringNode(pNode.children[i+1])
            else:
                self.validate("Atom", pNode.children[i+1])
                nextNode = self.genClassExp(pNode.children[i+1].children)
            parent.setFirstExp(tNode)
            parent.setSecondExp(nextNode)
            tNode = parent
            i += 2
        return tNode

################################################################################################

# Static Checker

################################################################################################
        
class MethodInfo:
    id:str
    returnType:str
    formals:'dict[str,str]'
    actuals:'dict[str,str]'
    argTypes:'tuple[str]'

class ClassInfo:
    cname:str
    fields:'dict[str,str]'
    msigs:'dict[str,dict[tuple[str],MethodInfo]]'
        
class ClassDescriptor:
    classTypes:'dict[str,ClassInfo]'

class Checker:
    def loadAST(self, ast:AST):
        self.ast = ast
        self.cd = ClassDescriptor()

    def checkNames(self):
        self.cd.classTypes = self.checkClassNames(self.ast.root)

    def checkClassNames(self, programNode:ProgramNode) -> 'dict[ClassInfo]':
        classTypes = {}

        # Check main class
        classInfo = ClassInfo()
        classInfo.cname = programNode.mainClass.cname
        classInfo.fields = self.checkClassFieldNames(programNode.mainClass)
        classInfo.msigs = self.checkClassMethodNames(programNode.mainClass)
        classTypes[classInfo.cname] = classInfo

        # Check all other classes
        for c in programNode.classes:
            info = ClassInfo()
            if c.cname in classTypes:
                errorF(f'error: repeated classname \'{c.cname}\' declaration not allowed')
            info.cname = c.cname
            info.fields = self.checkClassFieldNames(c)
            info.msigs = self.checkClassMethodNames(c)
            classTypes[info.cname] = info
        
        return classTypes

    def checkClassFieldNames(self, classNode:ClassNode):
        fields = {}
        for c in classNode.fields:
            if c.id in fields:
                errorF(f'error: repeated field \'{c.id}\' declaration in class \'{classNode.cname}\' not allowed')
            fields[c.id] = c.type
        return fields

    def checkClassMethodNames(self, classNode:ClassNode):
        msigs = {}
        """
        Use argTypes tuple as a key to uniquely identify the method signature
        """
        for m in classNode.methods:
            info = self.checkClassMethodParameterNames(m)
            if m.id in msigs and info.argTypes in msigs[m.id]:
                errorF(f'error: repeated method \'{m.id}\' with identical parameter(s) {info.argTypes} declaration in class \'{classNode.cname}\' not allowed')
            elif m.id in msigs:
                msigs[m.id][info.argTypes] = info
            else:
                msigs[m.id] = {info.argTypes : info}
        return msigs

    def checkClassMethodParameterNames(self, methodNode:MethodNode) -> MethodInfo:
        m = MethodInfo()
        m.id = methodNode.id
        m.returnType = methodNode.retType
        m.formals = {}
        m.actuals = {}
        argTypes = []
        for f in methodNode.formals:
            if f.id in m.formals:
                errorF(f'error: repeated formal parameter \'{f.id}\' in method \'{m.id}\' not allowed')
            m.formals[f.id] = f.type
            argTypes.append(f.type)
        for a in methodNode.actuals:
            if a.id in m.actuals:
                errorF(f'error: repeated actual parameter \'{a.id}\' declaration in method \'{m.id}\' not allowed')
            if a.id in m.formals:
                errorF(f'error: actual parameter \'{a.id}\' overlaps formal parameter in method \'{m.id}\' not allowed')
            m.actuals[a.id] = a.type
        m.argTypes = tuple(argTypes)
        return m







if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Usage: python ast.py filename")
        print("Usage: ./ast.py filename")
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

