import tokenizer
from tokenizer import *
from symbol_table import  symbol_info
import sys
from Constant import *
from code_generator import *

_tokenizer = None
table = None

def init(tokenizer, symbol_table):
    global _tokenizer, table

    _tokenizer = tokenizer
    table = symbol_table
    computation()

# Todo: show warning for unitialized variable

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

def cur_token():
    return tokenizer.cur_token

def lookup():
    name = last_id()
    symbol = table.lookup(name)
    if not symbol:
        my_SyntaxError(name + " "+ UNDEFINE)
    
    return symbol

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
    cfg.generate_dot()

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
        assignment()
    
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

def assignment():
    match_or_error(LET) # Todo: double check. can be removed
    # LET token alredy been checked in the previous funciton
    # So, just consume it.
    next()
    designator()
    ident = last_id()
    match_or_error(ASSIGNOP)
    next()
    res = E()
    code_assignment(ident, res)

def func_call():
    args = []
    match_or_error(CALL)
    next()
    match_or_error(IDENTIFIER)
    func_name = last_id()
    lookup()
    next()

    if match(LPAREN):
        next()
        args.append(E())

        while match(COMMA):
            next()
            args.append(E())
        
        match_or_error(RPAREN)
        next()

    res =  code_func_call(func_name, args)

    return res


def if_statement():
    set_phix(True)
    match_or_error(IF)
    next()
    relation()
    prev_bb = get_bid()
    create_join_bb(-1, cfg.tree[prev_bb].var_stat)
    match_or_error(THEN)
    cfg.add_bb()
    jump_ins = get_pc()
    next()
    stat_sequence()
    left = get_max_bid()
    right = 0
    add_nop()
    
    code_else(prev_bb)
    if match(ELSE):
        set_phix(False)
        next()
        # code_else(prev_bb)
        stat_sequence()
        set_phix(True)
    
    right = get_max_bid()

    # # No else block. So close the if block
    # else:
    #     cfg.add_bb()
    #     cfg.tree[cfg.b_id].add_parent(cfg.b_id-2)
    #     cfg.tree[cfg.b_id -2].add_children(cfg.b_id)
    #     cfg.tree[cfg.b_id-2].e_label[cfg.b_id] = "branch"
    #     update_jump(jump_ins)
    add_join_bb(left, right, jump_ins)
    match_or_error(FI)
    pop_phi()
    next()

def while_statement():
    match_or_error(WHILE)
    next()
    join_bid = cfg.add_bb()
    relation()
    jump_ins = get_pc()
    insert_join_bb_while()
    match_or_error(DO)
    cfg.add_bb()
    set_phix(False)
    next()
    stat_sequence()
    link_up_while(join_bid, jump_ins)
    match_or_error(OD)
    
    next()

def return_statement():
    match_or_error(RETURN)
    next()
    E()

def relation():
    resL = 0
    resR = 0
    resL = E()
    match_or_error([EQOP, NOTEQOP, LTOP, LEQOP, GTOP, GEQOP])
    relOp = cur_token()
    next()
    resR = E()
    pc = code_relation(resL, resR, relOp)

    return
    

def designator():

    match_or_error(IDENTIFIER)
    lookup()
    name = last_id()
    next() # [
    while match(LSQR):
        next() 
        E()
        match_or_error(RSQR)
        next()

    return

def E():
    res = 0
    resL = 0
    resR = 0

    resL = T()
    # assert isinstance(resL)==True, "Should be a symbol"
    res = resL

    while(True):
        if match(ADDOP):
            next()
            resR = F()
            # assert isinstance(resR) == True, "should be a symbol"
            res = code_f2("add", resL, resR)

        elif match(SUBOP):
            next()
            resR = F()
            # assert isinstance(resR) == True, "should be a symbol"
            res = code_f2("sub", resL, resR)

        else:
            break

    return res

def T():
    # symbol = symbol_info()
    res =0
    resR = 0
    resL = 0
    
    resL = F()
    # assert isinstance(resL) == True, "Should be a symbol"
    res = resL
    
    while(True):
        if match(MULOP):
            next()
            resR = F()
            # assert isinstance(resR)==True, "Should be a symbol"
            res = code_f2("mul", resL, resR)

        elif match(DIVIDEOP):
            next()
            resR = F()
            # assert isinstance(resR) == True, "Should be a symbol"
            res = code_f2("div", resL, resR)

        else:
            break
    
    # symbol.val = res

    return res

def F():
    res = 0
    symbol = symbol_info()

    if match(LPAREN):
        next()
        res = E()
        match_or_error(RPAREN)
        next()

    elif match(INTEGER):
       res = code_constant(last_val())
       next()
    
    elif match(IDENTIFIER):
        designator()
        symbol = lookup()
        res = get_var_pointer(last_id())
        symbol.val = res
        res = symbol

    elif match(CALL):
        symbol = lookup()
        res = func_call()
        
    # symbol.val = res

    return res