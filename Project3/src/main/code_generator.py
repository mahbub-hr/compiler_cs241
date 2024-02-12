from Constant import *
from tokenizer import *

class instruction:
    def __init__(self, ins_id, opcode, x, y, bid=-1):
        self.ins_id = ins_id 
        self.opcode = opcode
        self.x = x
        self.y = y
        self.bid = bid

    def update_y(self, y):
        self.y = y

    def __eq__(self, other):
        if isinstance(other, instruction):
            return self.opcode == other.opcode and self. x == other.x and self.y == other.y
        
        return False

    def __str__(self):
        x = '('+ str(self.x) + ')' if self.x is not None else ""
        y = '('+ str(self.y) + ')' if self.y is not None else ""
        return f"{self.ins_id}: {self.opcode} {x} {y}"

        
class BB:
    def __init__(self, id):
        self.table = []
        self.phi_idx = -1
        self.op_ins = {}     
        self.var_stat = {}
        self.phi = {}
        self.id = id
        self.next = []
        self.prev = []
        self.e_label = {}
        self.df = {} # dominating factor

    def append(self, ins_id):
        for i in self.table:
            if ins_array[i] == ins_array[ins_id]:
                dec_pc()
                return i

        self.table.append(ins_id)

        return ins_id
    
    def append_phi(self, ins_id):
        self.phi_idx = self.phi_idx + 1
        self.table.insert(self.phi_idx, ins_id)

    def append_const(self, ins_id):
        for i in self.table:
            if ins_array[i].x == ins_array[ins_id].x:
                inc_negpc()
                return i
        
        self.table.append(ins_id)
        return ins_id

    def add_children(self, id):
        self.next.append(id)

    def add_parent(self, id):
        self.prev.append(id)

    def get_var_pointer(self, var):
        return self.var_stat.get(var, None)
    
    def update_var(self, var, ins_id):
        self.var_stat[var] = ins_id

    def add_nop(self, ins_id):
        self.append(ins_id)

    def update_xold(self, xold, xnew):
        for i in self.table:
            ins = ins_array[i]
            if ins.opcode != "phi":
                if ins.x == xold:
                    ins.x = xnew

                if ins.y == xold:
                    ins.y = xnew
                

    def dot_node(self):
        ins_str = ""

        for i in self.table:
            ins_str = ins_str + str(ins_array[i]) + "|"
        
        ins_str = "{" + ins_str[:len(ins_str)-1] + "}"

        return f"bb{self.id}[shape=record, label=\"<b>BB{self.id}|{ins_str}|{str(self.var_stat)}\"];"

    def dot_edge(self):
        str_ = ""
        for i in self.next:
           str_ = str_ + f'bb{self.id}:s->bb{i}:n[label={'"'+self.e_label.get(i, None)+'"'}];\n'

        return str_
    

    def print(self):
        print("=======> BB #", self.id, "\n")
        self.print_var_stat()
        
        for i in self.table:
            print(ins_array[i])

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
        self.phi = {}

    def inc_bid(self):
        self.b_id = self.b_id + 1

    def get_bid(self):
        return self.b_id

    def default(self):
        self.tree[self.b_id] = BB(self.b_id)
        self.add_bb()

    '''
    Add an immidiate basic block just after the last block
    '''
    def add_bb(self):
        parent = self.b_id
        self.b_id = self.b_id + 1
        self.tree[self.b_id] = BB(self.b_id)
        self.tree[self.b_id-1].add_children(self.b_id)
        self.tree[self.b_id].add_parent(self.b_id-1)
        self.tree[self.b_id].var_stat = dict(self.tree[parent].var_stat)
        self.tree[self.b_id-1].e_label[self.b_id] = "fall-through" 
        return self.b_id

    def add_bb_man(self, bid, bid_prev, e_label):
        if bid_prev not in self.tree:
            return None
        if bid not in self.tree:
            return None

        self.tree[bid].add_parent(bid_prev)
        self.tree[bid_prev].add_children(bid)
        self.tree[bid_prev].e_label[bid] = e_label
    
    def add_join_bb(self, join_bb, prev, e_label):
       self.tree[join_bb.id] = join_bb
       self.add_bb_man(join_bb.id, prev, e_label)

    def create_bb(self):
        self.inc_bid()
        bb = BB(self.b_id)
        self.tree[self.b_id] = bb
        bb.var_stat = dict(self.tree[self.b_id-1].var_stat)

        return bb

    def update_var(self, var, ins_id):
        self.tree[self.b_id].update_var(var, ins_id)

    def get_var_pointer(self, var):
        return self.tree[self.b_id].get_var_pointer(var)

    def add_instruction(self, ins_id):
        return self.tree[self.b_id].append(ins_id)

    def add_inst_bb(self, ins_id, b_id):
        self.tree[b_id].append(ins_id)

    def add_const_instruction(self, ins_id):
        return self.tree[0].append_const(ins_id)

    def update_xold(self, join_bid, xold, xnew):
        node = [join_bid]
        visited = {}

        while node:
            id = node.pop()
            node = node + self.tree[id].next
            if id not in visited:
                visited[id] = True
                self.tree[id].update_xold(xold, xnew)


    def generate_dot(self):
        id = 0
        node = ""
        edge = ""
        
        while id <= self.b_id:
            node = node + self.tree[id].dot_node() + "\n"
            edge = edge + self.tree[id].dot_edge()
            id =id + 1

        node = "digraph G{\n" + node + edge + "}"

        print(node)
        with open("graph.dot", "w") as f:
            f.write(node)

    def print(self):
        id = 0

        while id <= self.b_id:
            self.tree[id].print()
            id = id+1
            print("\n")

relOp_fall = {EQOP:"bne", NOTEQOP: "beq", GTOP:"ble", GEQOP:"blt", LTOP:"bge", LEQOP:"bgt"}
default_foo = {"InputNum": "read", "OutputNum":"write", "OutputNewLine":"writeNL"}
cfg = CFG()
ins_array = {}
pc = 0
neg_pc = 0
phi= {}
phi_x = True

phi_i=-1

def get_pc():
    return pc

def get_bid():
    return cfg.get_bid()

def get_max_bid():
    return max(cfg.tree.keys())

def set_phix(val):
    global phi_x 
    phi_x = val

def create_join_bb(bid, var_stat):
    global phi_i
    join_bb = BB(bid) 
    join_bb.var_stat = dict(var_stat)# VAR STATE?
    phi_i = phi_i + 1
    phi[phi_i] = join_bb

# work with if statement
def add_join_bb(left, right, pc_head):
    join_bb = top_phi()
    join_bb.id = max(left, right) + 1
    cfg.b_id = join_bb.id
    inc_pc()
    ins_array[pc] = instruction(pc, "bra", join_bb.table[0], None)
    cfg.tree[left].table.append(pc)
    cfg.add_join_bb(join_bb, left, "fall-through")
    ins_array[pc_head].update_y(max(cfg.tree[right].table))
    cfg.add_join_bb(join_bb, right, "branch")

def insert_join_bb_while():
    global phi_i
    join_bb = cfg.tree[cfg.b_id]
    phi_i = phi_i + 1
    phi[phi_i] = join_bb

def link_up_while(join_bid, jump_ins):
    inc_pc()
    ins_array[pc] = instruction(pc, "bra", cfg.tree[join_bid].table[0], None)
    cfg.add_instruction(pc)
    cfg.add_bb_man(join_bid, get_bid(), "branch")
    ins_array[jump_ins].update_y(pc+1)
    bb = cfg.create_bb()
    bb.var_stat = dict(cfg.tree[join_bid].var_stat)
    cfg.add_bb_man(bb.id, join_bid, "branch")

def pop_phi():
    global phi_i
    join_bb = phi[phi_i]
    phi_i = phi_i - 1

    return join_bb

def top_phi():
    join_bb = phi[phi_i]

    return join_bb

def inc_pc():
    global pc
    pc = pc + 1
    return pc

def dec_pc():
    global pc
    pc = pc -1
    return pc

def inc_negpc():
    global neg_pc
    neg_pc = neg_pc +1

def dec_neg_pc():
    global neg_pc

    neg_pc = neg_pc - 1

def update_jump(jump_ins):
    ins_array[jump_ins].y = pc + 1

def get_var_pointer(identifier):
    return cfg.get_var_pointer(identifier)

def add_nop():
    if not cfg.tree[cfg.b_id].table:
        inc_pc()
        ins_array[pc] = instruction(pc, "nop", None, None)
        cfg.tree[cfg.b_id].add_nop(pc)

def code_assignment(identifier, ins_id):
    # is there any case where xold is not in the dictionary
    xold = cfg.get_var_pointer(identifier)
    cfg.update_var(identifier, ins_id)
    temp =0
    if phi_i > -1: 
        join_bb = phi[phi_i]
        if identifier not in join_bb.phi:
            inc_pc()
            temp = pc
            ins_array[pc] = instruction(pc, "phi", xold, xold)
            join_bb.phi[identifier] = pc
            join_bb.append_phi(pc)
            join_bb.update_var(identifier, pc)
            # update all uses of xold by phi
            cfg.update_xold(join_bb.id, xold, pc)
        
        else:
            temp = join_bb.phi[identifier]
        
        # left operand or right operand
        if phi_x:
            ins_array[temp].x = ins_id
        
        else:
            ins_array[temp].y = ins_id

        # update all xold value

    return

def code_constant(val):
    dec_neg_pc()
    ins_array[neg_pc] = instruction(neg_pc, "const #", val, None)

    return cfg.add_const_instruction(neg_pc)

def code_func_call(name, args_list):
    inc_pc()
    if name in default_foo:
        name = default_foo[name]

    inst = instruction(pc, name, None, None)
    ins_array[pc] = inst
    cfg.add_instruction(pc)

    return pc

def code_f2(opcode, x, y):
    inc_pc()
    ins_array[pc] = instruction(pc, opcode, x, y)
    return cfg.add_instruction(pc)



def code_else(prev_bb):
    bb = cfg.create_bb()
    bb.var_stat = dict(cfg.tree[prev_bb].var_stat)
    cfg.add_bb_man(bb.id, prev_bb, "branch")
    return bb.id

def code_relation(resL, resR, relOp):
    inc_pc()
    ins_array[pc] = instruction(pc, "cmp", resL, resR)
    cfg.add_instruction(pc)
    inc_pc()
    ins = instruction(pc, relOp_fall[relOp], pc-1, "follow")
    ins_array[pc] = ins
    cfg.add_instruction(pc)   
    return pc

def print_cfg():
    print(f"\n        *** CFG ***         \n")
    if DEBUG:
        cfg.print()