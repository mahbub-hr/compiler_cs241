from Constant import *

class instruction:
    def __init__(self, ins_id, opcode, x, y):
        self.ins_id = ins_id 
        self.opcode = opcode
        self.x = x
        self.y = y 

    def print(self):
        print(f"{self.ins_id} {self.opcode} {self.x} {self.y}\n")
        
class bb:

    def __init__(self, id):
        self.table = []       
        self.var_stat = {}
        self.i = 0
        self.id = id
        self.next = []

    def append(self, ins_id):
        self.table.append(ins_id)

    def add_children(self, id):
        self.next.append(id)

    def get_var_pointer(self, var):
        return self.var_stat[var]
    
    def update_var(self, var, ins_id):
        self.var_stat[var] = ins_id

    def print(self):
        print("=======> BB #", self.id, "\n")
        self.print_var_stat()
        
        for i in self.table:
            ins_array[i].print()

    def print_var_stat(self):
        print("Variable state \n")

        for key, val in self.var_stat.items():
            print(f'{key}:{val}')

        print("\n")

class CFG:
    def __init__(self):
        self.tree = {}
        self.b_id = 0
        self.default()

    def default(self):
        self.tree[self.b_id] = bb(self.b_id)
        self.add_bb()

    def add_bb(self):
        self.b_id = self.b_id + 1
        self.tree[self.b_id] = bb(self.b_id)
        # self.tree[self.b_id-1].add_children(self.b_ido)

    def update_var(self, var, ins_id):
        self.tree[self.b_id].update_var(var, ins_id)

    def get_var_pointer(self, var):
        return self.tree[self.b_id].get_var_pointer(var)

    def add_instruction(self, ins_id):
        self.tree[self.b_id].append(ins_id)

    def add_const_instruction(self, ins_id):
        self.tree[0].append(ins_id)

    def print(self):
        id = 0

        while id <= self.b_id:
            self.tree[id].print()
            id = id+1
            print("\n")
  
cfg = CFG()
ins_array = {}
pc = 0
neg_pc = 0

def inc_pc():
    global pc

    pc = pc + 1

def dec_neg_pc():
    global neg_pc

    neg_pc = neg_pc - 1

def cur_pc():
    return pc - 1

def get_var_pointer(identifier):
    return cfg.get_var_pointer(identifier)

def code_assignment(identifier, ins_id):
    cfg.update_var(identifier, ins_id)
    pass

def code_constant(val):
    dec_neg_pc()
    ins_array[neg_pc] = instruction(neg_pc, "const #", val, None)
    cfg.add_const_instruction(neg_pc)

    return neg_pc

def code_func_call(name, args_list):
    inc_pc()
    inst = instruction(pc, name, None, None)
    ins_array[pc] = inst
    cfg.add_instruction(pc)

    return pc

def code_f2(opcode, x, y):
    inc_pc()
    ins_array[pc] = instruction(pc, opcode, x, y)
    cfg.add_instruction(pc)

    return pc

def code_if():

    return

def print_cfg():
    print(f"\n        *** CFG ***         \n")
    if DEBUG:
        cfg.print()