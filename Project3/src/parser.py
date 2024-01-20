import tokenizer
from tokenizer import *
from symbol_table import symbol_table, symbol_info
import sys
from Constant import *

_tokenizer = None
table = None

def my_SyntaxError(msg):
    print("Syntax Error:: Line ", tokenizer.line_count ,": ", msg,"\n")
    sys.exit(-1)
    pass

def next():
    _tokenizer.next_token()

def match(token):
    return tokenizer.cur_token == token
    
def match_or_error(token):
    if tokenizer.cur_token != token:
        my_SyntaxError()

def last_id():
    return _tokenizer.last_id

def last_val():
    return _tokenizer.last_val

def lookup():
    name = last_id()
    if not table.lookup(name):
        my_SyntaxError(name + " "+ UNDEFINE_VAR)
    
    return True

def insert():
    symbol = table.insert(last_id(), symbol_info.var_symbol(last_id(), 0))
    

def print_table():
    if DEBUG:
        table.print()

def computation():
    next()
    match_or_error(MAIN)
    res = 0
    next() # main
    var_declaration()

   
    func_declaration()
    # next()
    table.print()
    # stat_sequence()
    # next()
    # next()

def var_declaration():
    if match(VAR):
        next()
        

    elif match(ARRAY):
        next()
        match_or_error(LSQR)

        next()

        print("Array Size: ", _tokenizer.last_val, "\n")

        next()

        match_or_error(RSQR)

        next()
     
    else:
        return

    # Assume that it is a var only
    table.insert(last_id(), symbol_info.var_symbol(last_id(), 0))
    next()

    while match(COMMA):
        next()
        next()
       
def func_declaration():
    if match(VOID):
        print("Need to work on", "\n")

    if match(FUNCTION):
        table.enter_scope()
        next()
        match_or_error(IDENTIFIER)
        func_name = _tokenizer.last_id
        next()
        param_list = formal_param()
        table.insert(func_name, symbol_info.func_symbol(func_name, param_list))

def formal_param():
    match_or_error(LPAREN)
    
    param_list = []
    next()

    if match(IDENTIFIER):
        lookup(last_id())
        param_list.append(_tokenizer.last_id)
        next()

        while match(COMMA):
            next()
            match_or_error(IDENTIFIER)
            lookup(last_id())
            param_list.append(_tokenizer.last_id)
            next()
    
    match_or_error(RPAREN)

    return param_list

def E():
    res = 0
    res = T()
    while(True):
        if match(ADDOP):
            next()
            res = res + T()
        elif match(SUBOP):
            next()
            res = res - T()
        else:
            break

    return res

def T():
    res =0
    res = F()
    while(True):
        if match(MULOP):
            next()
            res = res*F()
        
        elif match(DIVIDEOP):
            next()
            res = res/F()

        else:
            break

    return res

def F():
    res =0
    if match(LPAREN_TOKEN):
        next()
        res = E()
        # next()
        if match(RPAREN_TOKEN):
            next()
        else:
            my_SyntaxError()

    elif match(INTEGER):
       res = _tokenizer.last_val
       next()
    
    elif cur_token == IDENTIFIER_TOKEN:
        res = _table.get_val(_tokenizer.last_id)
        next()
    else:
        my_SyntaxError()

    return res



def main(): 
    global _tokenizer, table
    sentence = "main \n var var1, var2     \nfunction ident(var1, var2)\n;"
    #sentence = input("Enter your expression: ")
    _tokenizer = tokenizer.Tokenizer(sentence)
    table = symbol_table()
    computation()
    print("Successfully Compiled\n")
    pass

if __name__ == "__main__":
    main()
