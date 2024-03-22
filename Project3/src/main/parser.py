import tokenizer
from tokenizer import *
from symbol_table import  symbol_info
import sys
from Constant import *
import code_generator
import reg_allocator
import copy
import symbol_table


_tokenizer = None
table = None

def init(tokenizer):
    global _tokenizer, table

    _tokenizer = tokenizer
    table = symbol_table.get_symbol_table()
    computation()
    code_generator.render_dot()
    reg_allocator.live_variable_analysis(code_generator.cfg_list)
    code_generator.render_dot("live_var")
    reg_allocator.allocate_register(code_generator.cfg_list)
    reg_allocator.render_dot(code_generator.cfg_list)


# Todo: show warning for unitialized variable

def my_SyntaxError(msg):
    print("Syntax Error:: Line ", tokenizer.line_count ,": ", msg,"\n")
    sys.exit(-1)
    pass

def semantics_error(msg):
    print("Program Error:: Line ", tokenizer.line_count ,": ", msg,"\n")
    sys.exit(-1)

    return

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
        my_SyntaxError(UNEXPECTED_TOKEN(tokenizer.token_mapping[token], tokenizer.token_mapping[tokenizer.cur_token]))

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
    symbol =  symbol_info.var_symbol(last_id())
    ret = table.insert(last_id(),symbol)

    if ret is not None:
        my_SyntaxError(last_id() + " " +ALREADY_DEFINE + str(symbol.line_count))
    
    return symbol

def insert_array(array_size):
    symbol =  symbol_info.array_symbol(last_id(), array_size)
    ret = table.insert(last_id(),symbol)

    if ret is not None:
        my_SyntaxError(last_id() + " " +ALREADY_DEFINE + str(symbol.line_count))

    return symbol

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
    code_generator.cfg =  code_generator.instantiate_main_CFG()
    stat_sequence()
    code_generator.cfg.tree[code_generator.cfg.b_id].delete_marked_instruction()
    code_generator.code_end()
    match_or_error(RCURL)
    next()
    match_or_error(PERIOD)
    code_generator.cfg_list.append(code_generator.cfg)
    

def var_declaration():
    symbol_list = []
    var = True
    array_size = []

    if match(VAR):
        var = True
        next()

# Else must be an array becuase of the checking in caller function
    else:
        var = False
        next()
        match_or_error(LSQR)
        next()
        array_size.append(_tokenizer.last_val)
        print("Array Size: ", _tokenizer.last_val, "\n")
        next()
        match_or_error(RSQR)
        next()

        while match(LSQR):
            next()
            array_size.append(_tokenizer.last_val)
            print("Array Size: ", _tokenizer.last_val, "\n")
            next()
            match_or_error(RSQR)
            next()

    match_or_error(IDENTIFIER)
    if var:
       symbol = insert_var()
       symbol_list.append(symbol)
    else:
        symbol = insert_array(array_size)
        constant_list.extend(symbol.stride)
    next()

    while match(COMMA):
        next()
        match_or_error(IDENTIFIER)
        if var:
            insert_var()
        else:
            symbol = insert_array(array_size)
            constant_list.extend(symbol.stride)
        next()

    match_or_error(SEMICOLON)
    next()

    return constant_list
       
def func_declaration():
    return_type = True
    if match(VOID):
        return_type = False
        next()

    match_or_error(FUNCTION)
    next()

    table.enter_scope()
    match_or_error(IDENTIFIER)
    func_name = _tokenizer.last_id
    next()

    param_list = formal_param()
    symbol = insert_func(func_name, param_list, return_type)
    match_or_error(SEMICOLON)
    next()

    code_generator.cfg = code_generator.CFG(code_generator.current_bid)
    code_generator.cfg.name = func_name
    code_generator.cfg_list.append(code_generator.cfg)
    param_list = code_generator.code_func_parameter(param_list)
    update_symbol(param_list)
    func_body()

    match_or_error(SEMICOLON)
    next()

    table.exit_scope()
    symbol.cfg = code_generator.cfg
    symbol.cfg.tree[symbol.cfg.b_id].delete_marked_instruction()
    code_generator.current_bid = code_generator.cfg.b_id+1
    table.insert(symbol.name, symbol)

    return

def formal_param():
    match_or_error(LPAREN)
    next()
    
    param_list = []

    if match(IDENTIFIER):
        param = insert_var()
        param_list.append(param)
        next()

        while match(COMMA):
            next()
            match_or_error(IDENTIFIER)
            param = insert_var()
            param_list.append(param)
            next()
    
    match_or_error(RPAREN)
    next()

    return param_list

def func_body():
    while match(VAR) or match(ARRAY):
        constant_list = var_declaration()
    
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
    lsymbol = designator()
    match_or_error(ASSIGNOP)
    next()
    rsymbol = E() # can be a function call like input from user.
    code_generator.code_assignment(lsymbol, rsymbol)
    table.update(lsymbol.name, lsymbol) 

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
        arg_symbol = E()
        if arg_symbol:
            if arg_symbol.val:
                args.append(arg_symbol.val) # Todo: use code constant
            
            else:
                # can be a variable or array
                addr = code_generator.code_get_var_addr(arg_symbol)
                args.append(addr)

        while match(COMMA):
            next()
            arg_symbol = E()
            if arg_symbol:
                if symbol.val:
                    args.append(arg_symbol.val)
            
                else:
                    addr = code_generator.code_get_var_addr(arg_symbol)
                    args.append(addr)
        
        match_or_error(RPAREN)
        next()
    
    res =  code_generator.code_func_call(func_name, args)

    if func_name not in code_generator.default_foo:
        # code_generator.cfg.tree[code_generator.get_bid()].add_func_call(symbol.cfg)
        code_generator.cfg.add_bb()
        # code_generator.cfg.tree[code_generator.get_bid()].add_func_return(symbol.cfg)

    # Model reutrn value as 1. retval(x) if the function has return type. then return 1 as addr     
    symbol.addr = res

    return symbol


def if_statement():
    prev_bid = code_generator.get_bid()
    prev_bb = code_generator.cfg.tree[prev_bid]

    join_bb = code_generator.create_join_bb(prev_bb)

    # If header block
    match_or_error(IF)
    next()
    relation()
    code_generator.cfg.tree[code_generator.get_bid()].type = IF_HEADER_BLOCK
    code_generator.cfg.tree[prev_bid].delete_marked_instruction()
    
    # Then block
    join_bb.phi_x_operand = True
    match_or_error(THEN)
    next()
    code_generator.cfg.add_bb()
    jump_ins = code_generator.get_pc()
    stat_sequence()
    left = code_generator.get_max_bid()
    right = 0
    code_generator.add_nop(code_generator.cfg.b_id)
    code_generator.cfg.tree[code_generator.get_bid()].delete_marked_instruction()

    # Else block
    code_generator.code_else(prev_bid)
    if match(ELSE):
        next()
        join_bb.phi_x_operand = False
        stat_sequence()
    
    code_generator.cfg.tree[code_generator.get_bid()].delete_marked_instruction()
    right = code_generator.get_max_bid()

    code_generator.add_join_bb(left, right, jump_ins)
    match_or_error(FI)
    code_generator.pop_phi()
    next()

def while_statement():
    code_generator.cfg.tree[code_generator.cfg.b_id].delete_marked_instruction()
    
    # While JOIN BLOCK
    join_bid = code_generator.cfg.add_bb()

    match_or_error(WHILE)
    next()
    relation()
    jump_ins = code_generator.get_pc()
    code_generator.insert_join_bb_while()
    code_generator.cfg.tree[code_generator.get_bid()].type = WHILE_JOIN_BB

    # Loop Body
    code_generator.cfg.tree[code_generator.cfg.b_id].delete_marked_instruction()
    code_generator.cfg.add_bb()
    code_generator.cfg.tree[join_bid].phi_x_operand = False
    
    match_or_error(DO)
    next()
    stat_sequence()
    match_or_error(OD)
    next()

    code_generator.link_up_while(join_bid, jump_ins)

def return_statement():
    match_or_error(RETURN)
    next()
    symbol = E()
    code_generator.code_return(symbol)
    return

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

    symbol.last_index = []
    while match(LSQR):
        next()
        res = E()

        # when res.val is known 
        if res.val:
            pc = code_generator.code_constant(res.val)
        
        else:
            # Todo: find value if found in var state
            pc = res.addr

        symbol.last_index.append(pc)
        match_or_error(RSQR)
        next()

    return copy.deepcopy(symbol)

def E():
    x = T()

    while(True):
        if match(ADDOP):
            next()
            y = F()
            x = code_generator.code_f2("add", x, y)
            x.name= "expression"
            x.kind = EXPRESSION

        elif match(SUBOP):
            next()
            y = F()
            x = code_generator.code_f2("sub", x, y)
            x.name= "expression"
            x.kind = EXPRESSION

        else:
            break

    return x

def T():
    x = F()

    while(True):
        if match(MULOP):
            next()
            y = F()
            x = code_generator.code_f2("mul", x, y)
            x.name = "term"
            x.kind = TERM
            
        elif match(DIVIDEOP):
            next()
            y = F()
            x = code_generator.code_f2("div", x, y)
            x.name= "term"
            x.kind = TERM

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
            code_generator.code_array_load(symbol)
        else:
            addr = code_generator.get_var_pointer(symbol.name)

            if addr:
                symbol.addr = addr

            elif symbol.var_type != VAR_PAR:
                info("Warning:: variable " + symbol.name +" is not initialized")

    elif match(CALL):
        symbol = func_call()
        if symbol.return_type == False:
            semantics_error(VOID_FUNC_USE(symbol.name))

    return symbol