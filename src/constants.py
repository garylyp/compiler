# CONSTANTS 
DATA_LABEL = "LC0"

INT_FORMATTER = "\"%d\\n\""
STR_FORMATTER = "\"%s\\n\""
NULL_STRING   = "\"\""
INT_NO_LINE_FORMATTER = "\"%d\""
WRITE_SPACE = "\"" + "\\0" * 8 + "\""


ARM_STMFD = "stmfd"
ARM_LDMFD = "ldmfd"
ARM_LDR = "ldr"
ARM_STR = "str"
ARM_MOV = "mov"
ARM_NEG = "neg"

ARM_CMP = "cmp"
ARM_B = "b"
ARM_BL = "bl"
ARM_BGT = "bgt"
ARM_BGE = "bge"
ARM_BLT = "blt"
ARM_BLE = "ble"
ARM_BEQ = "beq"
ARM_BNE = "bne"

ARM_RELOP_MAPPER = {
    "==" : ARM_BEQ,
    "!=" : ARM_BNE,
    ">"  : ARM_BGT,
    ">=" : ARM_BGE,
    "<"  : ARM_BLT,
    "<=" : ARM_BLE
}

ARM_ADD = "add"
ARM_SUB = "sub"
ARM_MUL = "mul"

ARM_ARITHOP_MAPPER = {
    "+" : ARM_ADD,
    "-" : ARM_SUB,
    "*"  : ARM_MUL,
    # "/" : ARM_DIV,
}

ARM_ZERO = "#0"
ARM_ONE = "#1"

ARM_PRINTF = "printf"
ARM_SCANF = "scanf"
ARM_MALLOC = "malloc"

INITITAL_STK_SPACE = 4