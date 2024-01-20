from tokenizer import * 

class symbol_info:
    def __init__(self, name=None, kind=None, val=None):
        self.name = name
        self.kind = kind
        self.val = val
        self.line_count = 0
        # self.addr = addr
        # self.regno = regno
        self.param_list=None

    def func_symbol(name, param_list, kind = FUNCTION):
        func = symbol_info()
        func.name = name
        func.param_list = param_list
        func.kind = kind
        func.line_count = tokenizer.line_count

        return func
    
    def var_symbol(name, val = 0, kind = VAR):
        var = symbol_info()
        var.name = name
        var.val = val
        var.kind = kind
        var.line_count = tokenizer.line_count

        return var

    def __str__(self):
        return f"<{self.kind}, {self.val}, {self.param_list}, {self.line_count}>"

class scope_table:
    def __init__(self, id):
        self.table = {}
        self.id= id
        pass

    def error(self, msg):
        print(msg, "\n")
        raise Exception("Error")

    def insert(self, identifier, symbol):
        if identifier in self.table:
            return self.table[identifier]

        self.table[identifier] = symbol

        return True

    def update(self, identifier, value):
        if identifier in self.table:
            self.table[identifier] = value

        else:
            error(identifier + " Not Found")

    def remove(self, identifier):
        if identifier in self.table:
            del self.table[identifier]
        
    def get_val(self, identifier):
        return self.table[identifier]

    def lookup(self, name):
        return name in self.table

    def print_table(self):
        for key in self.table:
            print("<", key, ", ", self.table[key], ">\n")

class symbol_table:
    def __init__(self):
        self.table = []
        self.id = 0
        self.current_scope = scope_table(self.id)
        self.table.append(self.current_scope)
        self.id = self.id + 1

    def enter_scope(self):
        self.current_scope = scope_table(self.id)
        self.table.append(self.current_scope)
        self.id = self.id + 1
        
        return

    def exit_scope(self):
        self.id = self.id -1 
        self.table.pop()
        self.current_scope = self.table[self.id]
        return

    def insert(self, name, symbol):
        return self.current_scope.insert(name, symbol)

    def lookup(self, name):
        id = self.id - 1

        while id >= 0:
            if self.table[id].lookup(name):
                return True
            
            id = id - 1

        return False

    def print(self):
        id = self.id-1

        while id >= 0:
            print("==> Scope #", id, "\n")
            self.table[id].print_table()
            id = id -1

