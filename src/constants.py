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

ARM_ZERO = "#0"
ARM_ONE = "#1"

ARM_MOV = "mov"