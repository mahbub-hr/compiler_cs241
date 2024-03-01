import tokenizer
from tokenizer import * 
from Constant import *

import copy

class symbol_info:

    def __init__(self, name=None, kind=None, val=None, addr= None):
        self.name = name
        self.kind = kind
        self.val = val
        self.line_count = 0
        # self.addr = addr
        # self.regno = regno
        self.param_list=None
        self.return_type = True

    def func_symbol(name, param_list, return_type=True, kind = FUNCTION):
        func = symbol_info()
        func.name = name
        func.cfg = None
        func.param_list = param_list
        func.kind = kind
        func.line_count = tokenizer.line_count
        func.return_type= return_type

        return func
    
    def var_symbol(name, val = None, addr = None, kind = VAR):
        var = symbol_info()
        var.name = name
        var.val = val
        var.addr = addr
        var.kind = kind
        var.line_count = tokenizer.line_count

        return var
    
    def array_symbol(name, size = 0, kind = ARRAY):
        var = symbol_info()
        var.name = name
        var.size = size
        var.kind = kind
        var.idx = {}
        var.base = f"{name}_base"
        var.line_count = tokenizer.line_count

        return var

    def const_symbol(name="Constant", val=0, kind = CONSTANT):
        const = symbol_info()
        const.name = name
        const.val = val
        const.kind = kind
        const.line_count = tokenizer.line_count

        return const

    def __str__(self):
        return f"<{self.kind}, {self.val}, {self.param_list}, {self.return_type}, {self.line_count}>"

class scope_table:
    def __init__(self, id):
        self.table = {}
        self.id= id
        pass

    def error(self, msg):
        print(msg, "\n")
        raise Exception("Error")

    '''
        On successful: return None
        IF exist: return the symbol
    '''
    def insert(self, identifier, symbol):
        if identifier in self.table:
            return self.table[identifier]

        self.table[identifier] = symbol

        return None

    def update(self, identifier, symbol):
        if identifier in self.table:
            self.table[identifier] = symbol

        else:
            error(identifier + " Not Found")

    def remove(self, identifier):
        if identifier in self.table:
            del self.table[identifier]
        
    def get_val(self, identifier):
        return self.table[identifier]

    def lookup(self, name):
        if name in self.table:
            return self.table[name]

        return None

    def print_table(self):
        for key in self.table:
            print("<", key, ", ", self.table[key], ">\n")

class symbol_table:
    def __init__(self):
        self.table = []
        self.id = 0
        self.current_scope = scope_table(self.id)
        self.table.append(self.current_scope)
        self.insert_default()

    def insert_default(self):
        inputNum = symbol_info.func_symbol("InputNum", [], return_type=False)
        self.current_scope.insert("InputNum", inputNum)
        
        outputNum = symbol_info.func_symbol("OutputNum", ["x"], return_type= False)
        self.current_scope.insert("OutputNum", outputNum) 

        outputNewLine = symbol_info.func_symbol("OutputNewLine", [], return_type= False)
        self.current_scope.insert("OutputNewLine", outputNewLine)
        

    def enter_scope(self):
        self.id = self.id + 1
        self.current_scope = scope_table(self.id)
        self.table.append(self.current_scope)
        
        return

    def exit_scope(self):
        self.id = self.id -1 
        self.table.pop()
        self.current_scope = self.table[self.id]
        return

    '''
        On successful: return None
        IF exist: return the symbol
    '''
    def insert(self, name, symbol):
        return self.current_scope.insert(name, symbol)

    def update(self, name, symbol):
        sym = self.lookup(name)

        if sym is not None:
            self.current_scope.update(name, symbol)

        return sym

    def lookup(self, name):
        id = self.id 

        while id >= 0:
            symbol = self.table[id].lookup(name)
            if symbol:
                return symbol
            
            id = id - 1

        return None

    def print(self):
        id = self.id

        while id >= 0:
            print("==> Scope #", id, "\n")
            self.table[id].print_table()
            id = id -1

