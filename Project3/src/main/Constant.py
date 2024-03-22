DEBUG = True
CSE = False
UNDEFINE = "undefine"
ALREADY_DEFINE = "already defined at line #"
UNRECOG_SYM = "unrecognize symbol"

def VOID_FUNC_USE(name):
    "Use of a void function " + name +" is not allowed"
    return
    
def UNEXPECTED_TOKEN(expected, unexpected):
    return f"expected {expected} but found {unexpected}"

def debug(msg):
    if DEBUG:
        print(msg, "\n")

def info(msg):
    print(msg, "\n")

# Symbol 
VAR_PAR = 0
VAR_REG = 1

# TokenizerPERIOD = -1
ADDOP = 1
SUBOP = 2
MULOP = 3
DIVIDEOP = 4
LPAREN = 5
RPAREN = 6
COMPUTATION= 7
IDENTIFIER = 8
SEMICOLON = 9
VAR = 10
ASSIGNOP = 11
INTEGER = 12
LSQR = 13
RSQR = 14
LCURL = 15
RCURL = 16
COMMA = 17
EQOP = 18
NOTEQOP = 19
LEQOP = 20
GEQOP = 21
LTOP = 22
GTOP = 23
LET = 24
CALL = 25
IF = 26
THEN = 27
ELSE = 28
FI = 29
WHILE = 30
DO = 31
OD = 32
RETURN = 33
ARRAY = 34
VOID = 35
FUNCTION = 36
MAIN = 37
CONSTANT = 38
EXPRESSION = 39
TERM = 40

token_name = {
    ADDOP: "+",
    SEMICOLON: ";",
    COMMA : ",",
    RCURL: "}",
    LCURL: "{"
}
# Code Generator
# opcode
BP = "bp"
CONST_ZERO_ADDR = -1
CONST_FOUR_ADDR = -2
IF_JOIN_BB_ID = -1 # Replace this
CONST_BB_ID = 0
IF_JOIN_BLOCK = 1
WHILE_JOIN_BB = 2
IF_HEADER_BLOCK = 3
ELSE_BLOCK = 4
INSTRUCTION = 7
PSEUDO_INSTRUCTION= 8
PHI_START_IDX = -1

opcode = {
    "add": 1,
    "sub": 2, 
    "mul": 3,
    "div": 4,
    "cmp": 5,
    "adda": 6,
    "load": 7,
    "store": 8,
    "phi": 9,
    "end": 10,
    "bra": 11,
    "bne": 12,
    "beq": 13,
    "ble": 14,
    "blt": 15,
    "bge": 16,
    "bgt": 17,
    "jsr": 18,
    "ret": 19
}
BRACH_OPCODE = {"bne", "beq", "ble", "blt", "bge", "bgt", "bra"}
# relOp_fall = {EQOP:"bne", NOTEQOP: "beq", GTOP:"ble", GEQOP:"blt", LTOP:"bge", LEQOP:"bgt"}
# default_foo = {"InputNum": "read", "OutputNum":"write", "OutputNewLine":"writeNL"}
# ins_array = {}
# pc = 0
# neg_pc = 0
# phi= {}

# phi_i=-1


#########################################
#       Register Allocator              # 
#                                       #
#########################################
ALLOCATED = True
NOT_ALLOCATED = False
VIRTUAL_REG = True
PHYSICAL_REG = True
PHY_REG_START = 0
VIR_REG_END = 100
NO_PHY_REG_AVAILABLE = -1
NO_VIR_REG_AVAILABLE = -1
# Machine Config
NO_OF_GPR = 5 