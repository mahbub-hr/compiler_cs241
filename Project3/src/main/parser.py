import tokenizer
from tokenizer import *
from symbol_table import  symbol_info
import sys
from Constant import *

_tokenizer = None
table = None

def init(tokenizer, symbol_table):
    global _tokenizer, table

    _tokenizer = tokenizer
    table = symbol_table
    computation()


def my_SyntaxError(msg):
    print("Syntax Error:: Line ", tokenizer.line_count ,": ", msg,"\n")
    sys.exit(-1)
    pass

def next():
    _tokenizer.next_token()

def back():
    _tokenizer.step_back()

def match(token):
    return tokenizer.cur_token == token
    
def match_or_error(token):
    token_array =[]
    if isinstance(token, int):
        token_array.append(token)
    else:
        token_array = token

    if tokenizer.cur_token not in token_array:
        my_SyntaxError(UNEXPECTED_TOKEN(token, tokenizer.cur_token))

def last_id():
    return _tokenizer.last_id

def last_val():
    return _tokenizer.last_val

def lookup():
    name = last_id()
    if not table.lookup(name):
        my_SyntaxError(name + " "+ UNDEFINE)
    
    return True

def insert_var():
    symbol = table.insert(last_id(), symbol_info.var_symbol(last_id(), 0))

    if symbol is not None:
        my_SyntaxError(last_id() + " " +ALREADY_DEFINE + str(symbol.line_count))

def insert_func(func_name, param_list, return_type):
    symbol = table.insert(func_name,symbol_info.func_symbol(func_name, param_list, return_type))

    if symbol is not None:
        my_SyntaxError(func_name + " " +ALREADY_DEFINE + symbol.line_count)




def print_table():
    if DEBUG:
        table.print()

def computation():
    next()
    match_or_error(MAIN)
    res = 0
    next() # main

    while match(VAR) or match(ARRAY):
        var_declaration()
    
    while match(FUNCTION) or match(VOID):
        func_declaration()

    table.print()
    match_or_error(LCURL)
    next()
    stat_sequence()
    match_or_error(RCURL)
    next()
    match_or_error(PERIOD)

def var_declaration():
    if match(VAR):
        next()   

# Else must be an array becuase of the checking in caller function
    else:
        next()
        match_or_error(LSQR)
        next()

        print("Array Size: ", _tokenizer.last_val, "\n")
        next()
        match_or_error(RSQR)
        next()

    # Assume that it is a var only
    insert_var()
    next()

    while match(COMMA):
        next()
        insert_var()
        next()

    match_or_error(SEMICOLON)
    next()
       
def func_declaration():
    return_type = True
    if match(VOID):
        print("Need to work on", "\n")
        return_type = False
        next()

    match_or_error(FUNCTION)

    table.enter_scope()
    next()
    match_or_error(IDENTIFIER)
    func_name = _tokenizer.last_id
    next()
    param_list = formal_param()
    insert_func(func_name, param_list, return_type)
    match_or_error(SEMICOLON)
    next()
    func_body()
    match_or_error(SEMICOLON)
    next()
    table.exit_scope()

def formal_param():
    match_or_error(LPAREN)
    next()
    
    param_list = []

    if match(IDENTIFIER):
        lookup()
        param_list.append(_tokenizer.last_id)
        next()

        while match(COMMA):
            next()
            match_or_error(IDENTIFIER)
            lookup()
            param_list.append(_tokenizer.last_id)
            next()
    
    match_or_error(RPAREN)
    next()

    return param_list

def func_body():
    while match(VAR) or match(ARRAY):
        var_declaration()
    
    match_or_error(LCURL)
    next()
    stat_sequence()
    match_or_error(RCURL)
    next()

def stat_sequence():
    statement()
    
    while match(SEMICOLON):
        next()
        '''
            Since this semicolon is optional, check whether actually there are statements
        '''
        if match(LET) or match(CALL) or match(IF) or match(WHILE) or match(RETURN):
            statement()

    if match(LET) or match(CALL) or match(IF) or match(WHILE) or match(RETURN):
        my_SyntaxError(UNEXPECTED_TOKEN(SEMICOLON, tokenizer.cur_token))
    
    return

def statement():
    if match(LET):
        assingment()
    
    elif match(CALL):
        func_call()

    elif match(IF):
        if_statement()
    
    elif match(WHILE):
        while_statement()

    elif match(RETURN):
        return_statement()
    
    else:
        # stateSequence is optional. So, Not a syntax error
        return

def assingment():
    match_or_error(LET) # Todo: double check. can be removed
    # LET token alredy been checked in the previous funciton
    # So, just consume it.
    next()
    designator()
    match_or_error(ASSIGNOP)
    next()
    E()

def func_call():
    match_or_error(CALL)
    next()
    match_or_error(IDENTIFIER)
    lookup()
    next()

    if match(LPAREN):
        next()
        E()
        while match(COMMA):
            E()
        
        match_or_error(RPAREN)
        next()

def if_statement():
    match_or_error(IF)
    next()
    relation()
    match_or_error(THEN)
    next()
    stat_sequence()
    
    if match(ELSE):
        next()
        stat_sequence()
    
    match_or_error(FI)
    next()

def while_statement():
    match_or_error(WHILE)
    next()
    relation()
    match_or_error(DO)
    next()
    stat_sequence()
    match_or_error(OD)
    next()

def return_statement():
    match_or_error(RETURN)
    next()
    E()

def relation():
    E()
    match_or_error([EQOP, NOTEQOP, LTOP, LEQOP, GTOP, GEQOP])
    next()
    E()

    return
    

def designator():
    match_or_error(IDENTIFIER)
    next() # [
    while match(LSQR):
        next() 
        E()
        match_or_error(RSQR)
        next()


def E():
    res = 0
    res = T()

    while(True):
        if match(ADDOP):
            next()
            T()
        elif match(SUBOP):
            next()
            T()
        else:
            break

    return res

def T():
    res =0
    res = F()

    while(True):
        if match(MULOP):
            next()
            F()
        
        elif match(DIVIDEOP):
            next()
            F()

        else:
            break

    return res

def F():
    res =0

    if match(LPAREN):
        next()
        res = E()
        match_or_error(RPAREN)

    elif match(INTEGER):
       res = _tokenizer.last_val
       next()
    
    elif match(IDENTIFIER):
        designator()
        res = table.lookup(_tokenizer.last_id)

    elif match(CALL):
        func_call()

    return res