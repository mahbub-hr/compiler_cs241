import tokenizer
from tokenizer import *
from symbol_table import  symbol_info
import sys
from Constant import *
import code_generator

import copy 


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
    symbol = table.insert(last_id(), symbol_info.var_symbol(last_id()))

    if symbol is not None:
        my_SyntaxError(last_id() + " " +ALREADY_DEFINE + str(symbol.line_count))

def insert_array():
    symbol = table.insert(last_id(), symbol_info.array_symbol(last_id(), last_val()))

    if symbol is not None:
        my_SyntaxError(last_id() + " " +ALREADY_DEFINE + str(symbol.line_count))

def insert_func(func_name, param_list, return_type):
    sym = symbol_info.func_symbol(func_name, param_list, return_type)
    ret = table.insert(func_name,sym)

    if ret is not None:
        my_SyntaxError(func_name + " " +ALREADY_DEFINE + symbol.line_count)

    return sym


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
    code_generator.instantiate_main_CFG()
    stat_sequence()
    match_or_error(RCURL)
    next()
    match_or_error(PERIOD)
    code_generator.cfg.render_dot()

def var_declaration():
    if match(VAR):
        next()
        insert = insert_var 

# Else must be an array becuase of the checking in caller function
    else:
        insert = insert_array
        # Todo: Implement multi dimentional array
        next()
        match_or_error(LSQR)
        next()

        print("Array Size: ", _tokenizer.last_val, "\n")
        code_constant(last_val())
        next()
        match_or_error(RSQR)
        next()

    # Assume that it is a var only
    insert()
    next()

    while match(COMMA):
        next()
        insert()
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
    symbol = insert_func(func_name, param_list, return_type)
    match_or_error(SEMICOLON)
    next()
    code_generator.cfg = code_generator.CFG()
    func_body()
    match_or_error(SEMICOLON)
    next()
    table.exit_scope()
    symbol.cfg = code_generator.cfg
    table.insert(symbol.name, symbol)


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
    symbol = designator()
    match_or_error(ASSIGNOP)
    next()
    res = E() # can be a function call like input from user.
    
    if symbol.kind == ARRAY:
        symbol = code_array_store(symbol, res)
        table.update(symbol.name, symbol)
        
    code_generator.code_assignment(symbol, res)

def func_call():
    args = []
    match_or_error(CALL)
    next()
    match_or_error(IDENTIFIER)
    func_name = last_id()
    symbol = lookup()
    next()

    if match(LPAREN):
        next()
        args.append(E())

        while match(COMMA):
            next()
            args.append(E())
        
        match_or_error(RPAREN)
        next()
    res =  code_generator.code_func_call(func_name, args)

    # code_generator.cfg.tree[code_generator.get_bid()].call_foo = symbol.cfg
    code_generator.cfg.add_bb()
    symbol.addr = res

    return symbol


def if_statement():
    code_generator.set_phix(True)
    match_or_error(IF)
    next()
    relation()
    prev_bb = code_generator.get_bid()
    code_generator.cfg.tree[prev_bb].delete_marked_instruction()
    code_generator.create_join_bb(IF_JOIN_BB_ID, cfg.tree[prev_bb].var_stat)
    match_or_error(THEN)
    code_generator.cfg.add_bb()
    jump_ins = get_pc()
    next()
    stat_sequence()
    left = code_generator.get_max_bid()
    right = 0
    add_nop(cfg.b_id)
    code_generator.cfg.tree[get_bid()].delete_marked_instruction()
    code_generator.code_else(prev_bb)
    if match(ELSE):
        code_generator.set_phix(False)
        next()
        # code_else(prev_bb)
        stat_sequence()
        code_generator.set_phix(True)
    
    code_generator.cfg.tree[code_generator.get_bid()].delete_marked_instruction()
    right = code_generator.get_max_bid()

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
    code_generator.cfg.tree[code_generator.cfg.b_id].delete_marked_instruction()
    join_bid = code_generator.cfg.add_bb()
    relation()
    jump_ins = code_generator.get_pc()
    code_generator.insert_join_bb_while()
    match_or_error(DO)
    code_generator.cfg.tree[code_generator.cfg.b_id].delete_marked_instruction()
    code_generator.cfg.add_bb()
    code_generator.set_phix(False)
    next()
    stat_sequence()
    code_generator.link_up_while(join_bid, jump_ins)
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
    pc = code_generator.code_relation(resL, resR, relOp)

    return
    
def designator():

    match_or_error(IDENTIFIER)
    symbol = lookup()
    next() # [
    while match(LSQR):
        next()
        res = E()

        # when res.val is known 
        if res.val:
            pc = code_constant(res.val)
        
        else:
            pc = res.addr

        symbol.temp = pc
        match_or_error(RSQR)
        next()

    return copy.deepcopy(symbol)

def E():
    x = T()

    while(True):
        if match(ADDOP):
            next()
            y = F()
            x.val = code_generator.compute(ADDOP, x, y)
            x.addr = code_generator.code_f2("add", x, y)
            x.name= "computation"

        elif match(SUBOP):
            next()
            y = F()
            x.val = code_generator.compute(SUBOP, x, y)
            x.addr = code_generator.code_f2("sub", x, y)
            x.name= "computation"

        else:
            break

    return x

def T():
    x = F()

    while(True):
        if match(MULOP):
            next()
            y = F()
            x.val = code_generator.compute(MULOP, x, y)
            x.addr = code_generator.code_f2("mul", x, y)
            x.name = "computation"
            
        elif match(DIVIDEOP):
            next()
            y = F()
            x.val = code_generator.compute(DIVIDEOP, x, y)
            x.addr = code_generator.code_f2("div", x, y)
            x.name= "computation"
        else:
            break

    return x

def F():
    symbol = None

    if match(LPAREN):
        next()
        symbol = E()
        match_or_error(RPAREN)
        next()

    elif match(INTEGER):
        symbol = symbol_info.const_symbol(val= last_val())
        symbol.addr = code_generator.code_constant(last_val())
        next()
    
    elif match(IDENTIFIER):
        symbol = designator()
        # avoid duplicate array load
        if symbol.kind == ARRAY:
            code_array_load(symbol)
        else:
            symbol.addr = code_generator.get_var_pointer(symbol.name)
            
    elif match(CALL):
        symbol = func_call()

    return symbol