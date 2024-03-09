from Constant import *
from tokenizer import *
from symbol_table import *
import json

class instruction:
    def __init__(self, ins_id, opcode, x, y, type_ = None, bid=-1):
        self.ins_id = ins_id 
        self.opcode = opcode
        self.x = x
        self.y = y
        self.bid = bid
        self.type = type_
        self.add_operand_usage(x)
        self.add_operand_usage(y)

    def add_operand_usage(self, x):
        if x in ins_ref_list:
            if self.ins_id not in ins_ref_list[x]:
                ins_ref_list[x].append(self.ins_id)
        else:
            ins_ref_list[x] = [self.ins_id]

    def update_y(self, y):
        # ins_ref_list[y].remove(self.ins_id)
        self.add_operand_usage(y)
        self.y = y

    def update_x(self, x):
        # ins_ref_list[x].remove(self.ins_id)
        self.add_operand_usage(x)
        self.x = x

    def __eq__(self, other):
        if isinstance(other, instruction):
            return self.type != FUNCTION and self.opcode == other.opcode and self. x == other.x and self.y == other.y
        
        return False

    def __str__(self):
        x = '('+ str(self.x) + ')' if self.x is not None else ""
        y = '('+ str(self.y) + ')' if self.y is not None else ""
        return f"{self.ins_id}: {self.opcode} {x} {y}"

def dict_str(d, indent):
    result = ""
    for key, value in d.items():
        result += "  " * indent + str(key) + ": "
        if isinstance(value, dict):
            result += "\n" + dict_str(value, indent + 1)
        else:
            result += str(value) + "\n"
    return result

def set_str(s):
    return ", ".join(str(e) for e in s)
        
class BB:
    def __init__(self, id):
        self.call_foo = None
        self.type = None
        self.phi_direction = None
        self.table = []
        self.phi_idx = -1
        self.var_usage = {}     
        self.var_stat = {}
        self.live_var_set = {}
        # {var: ins_id}
        self.phi = {}
        self.id = id
        self.next = []
        self.prev = []
        #function call & return
        self.func_call=[]
        self.func_return= []

        self.e_label = {}
        self.dom_block = []
        self.dom_instruction = {} # dominating factor
        '''{dom_ins: [simillar dominated instructions], ..}'''
        self.marked_for_deleted= {} 

    def is_empty(self):
        if self.table:
            return False
        
        return True

    def add_dom_instruction(self, opcode, ins_id):
        opcode_to_excl = ['read', 'phi', 'bra']

        if opcode in opcode_to_excl:
            return None

        if opcode not in self.dom_instruction:
            self.dom_instruction[opcode] = []

        self.dom_instruction[opcode].append(ins_id)


    def find_dom_instruction(self, instruction):
        '''Return the equivalent dominating instruction id'''

        if instruction.opcode not in self.dom_instruction:
            return None

        ins_list = self.dom_instruction[instruction.opcode]

        for i in range(len(ins_list)-1, -1, -1):
            if ins_array[ins_list[i]] == instruction:
                return ins_list[i]
            
        return None
    
    def delete_marked_instruction(self):
        for ins in self.marked_for_deleted:
            # these instructions will be deleted
            marked_for_deleted = self.marked_for_deleted[ins]
            for i in marked_for_deleted:
                # operands might change, recheck for equivalence again
                if ins_array[ins] == ins_array[i]:
                    self.update_var_with_new_ins(i, ins)
                    self.table.remove(i)
                    usage = ins_ref_list[i]
                    for u in usage:
                        if ins_array[u].x == i:
                            ins_array[u].update_x(ins)
                        if ins_array[u].y == i:
                            ins_array[u].update_y(ins)

                    
                    
    '''Update var_stat with new instruction id'''
    def update_var_with_new_ins(self, prev_id, new_id):
        for var in self.var_stat:
            if prev_id == self.var_stat[var]:
               self.update_var(var, new_id)
               var_usage = self.var_usage[var]

        return

    def append(self, ins_id):
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
    
    def append_inst_without_cse(self, ins_id):
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

    def update_array(self, var, idx, ins_id):
        if var not in self.var_stat:
            self.var_stat[var] = {}

        self.var_stat[var][idx] = ins_id
    
    def update_var_usage(self, var, ins_id):
        if var not in self.var_usage:
            self.var_usage[var] = [ins_id]
        else:
            self.var_usage[var].append(ins_id)

    # Success: return the var name
    # Fail: return None
    def remove_var_usage(self, var, ins_id):
        if var in self.var_usage:
            self.var_usage[var].remove(ins_id)

            return var

        return None
    def get_parent(self):
        return self.prev

    # def get_parent_with_larger_bid(self):
    #     return self.prev[:-1]

    # def get_parent_with_smaller_bid(self):
    #     return self.prev[0]

    def add_live_var_set(self, prev_live_var_set):
        if self.table[-1] in self.live_var_set:
            self.live_var_set[self.table[-1]] = self.live_var_set[self.table[-1]].union(prev_live_var_set)

        else:
            self.live_var_set[self.table[-1]] = set(prev_live_var_set)

        return
    
    def get_phi_x_operand_set(self):
        x_operand_set = set()
        for i in self.phi.values():
            x_operand_set.add(ins_array[i].x)
        
        return x_operand_set

    def get_phi_y_operand_set(self):
        y_operand_set = set()
        for i in self.phi.values():
            y_operand_set.add(ins_array[i].y)
        
        return y_operand_set
            
    def live_variable_analysis(self):
        s = self.live_var_set[self.table[-1]] # Todo: live from next bb
        
        for i in reversed(self.table):
            if i in self.phi.values():
                s.discard(i)
                continue

            if ins_array[i].x is not None and ins_array[i].x>0:# >0 means not a constant
                s.add(ins_array[i].x)

            if ins_array[i].y is not None and ins_array[i].y>0:
                s.add(ins_array[i].y)
            
            s.discard(i)

            self.live_var_set[i] = set(s)
            
        return s


    def add_nop(self, ins_id):
        self.append(ins_id)

    def bb_copy(self):

        return

    def update_xold(self, var, xold, xnew):
        try:
            for i in self.var_usage[var]:
                ins = ins_array[i]
                if ins.opcode != "phi":
                    if ins.x == xold:
                        ins.x = xnew

                    if ins.y == xold:
                        ins.y = xnew

        except:
            pass
                
    def add_func_call(self, cfg):
        self.call_foo = cfg
        self.func_call.append(cfg.init_bid) # Todo: store func call in a seperate list?

    def add_func_return(self, cfg):
        self.func_return.append(cfg.b_id)

    def dot_node(self):
        ins_str = ""
        live_var = ""

        for i in self.table:
            ins_str = ins_str + str(ins_array[i]) + "|"
            live_var = live_var + (set_str(self.live_var_set[i]) if i in self.live_var_set else "") + "|"
        
        ins_str = "{" + ins_str[:len(ins_str)-1] + "}|{" + live_var[:len(live_var)-1]+"}"
        var_stat_str = dict_str(self.var_stat, 2) 
        var_usage_str = dict_str(self.var_usage, 2)

        state = "{"+ var_stat_str + '}' +'|{'+  var_usage_str + "}"
        cur_node_str = f"bb{self.id}[shape=record, label=\"<b>BB{self.id}|{ins_str}|{state}\"];"
        

        return cur_node_str
        
    def dot_edge(self):
        str_ = ""
        foo_node=""
        foo_edge = ""
   
        for i in self.next:
           str_ = str_ + f'bb{self.id}:s->bb{i}:n[label={'"'+self.e_label.get(i, None)+'"'}];\n'

        for i in self.func_call:
            str_ = str_ + f'bb{self.id}->bb{i}[label="function-call"];\n'

        for i in self.func_return:
            str_ = str_ + f'bb{i}->bb{self.id}[label= "function-return"];\n'

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
    def __init__(self, init_bid):
        self.tree = {}
        self.b_id = init_bid
        self.init_bid = init_bid
        self.phi = {}
        self.default()

    def inc_bid(self):
        self.b_id = self.b_id + 1

    def get_bid(self):
        return self.b_id

    def min_bid(self):
        return min(self.tree.keys())

    def max_bid(self):
        return self.b_id

    def default(self):
        global neg_pc
        self.tree[self.b_id] = BB(self.b_id)
        self.add_bb()

    '''
    Add an immidiate basic block just after the last block
    CFG grows linearly
    '''
    def add_bb(self):
        parent = self.b_id
        # No Need to create a new block
        if parent>CONST_BB_ID and self.tree[parent].is_empty():
            return parent

        self.b_id = self.b_id + 1
        bb = BB(self.b_id)
        self.tree[self.b_id] = bb
        self.tree[self.b_id-1].add_children(self.b_id)
        self.tree[self.b_id].add_parent(self.b_id-1)
        self.tree[self.b_id].var_stat = dict(self.tree[parent].var_stat)
        self.tree[self.b_id-1].e_label[self.b_id] = "fall-through"
        # dominator
        bb.dom_block.append(parent)

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

    def remove__bb(self):
        self.b_id = self.b_id-1

    def update_var(self, var, ins_id):
        self.tree[self.b_id].update_var(var, ins_id)
    
    def update_array(self, var, idx, ins_id):
        self.tree[self.b_id].update_array(var, idx, ins_id)

    def update_var_usage(self, var, ins_id):
        self.tree[self.b_id].update_var_usage(var, ins_id)

    def get_var_pointer(self, var):
        return self.tree[self.b_id].get_var_pointer(var)
    
    def find_dom_instruction(self, instruction):
        bid = self.b_id
        while bid is not None and bid > self.init_bid:
            bb = self.tree[bid]
            ins_id = bb.find_dom_instruction(instruction)
            if ins_id:
                return ins_id
            
            # search in the next dominator
            bid = bb.dom_block[0] if bb.dom_block else None # 0--> first dominator

        # finished searching up to top-most dominator
        return None

    def add_instruction(self, ins_id):
        # find the dominating instruction
        instruction = ins_array[ins_id]
        dom_ins_id = self.find_dom_instruction(instruction)

        if dom_ins_id:
            marked_for_deleted =  self.tree[self.b_id].marked_for_deleted
            if dom_ins_id in marked_for_deleted:
                marked_for_deleted[dom_ins_id].append(ins_id)
            
            else: 
                marked_for_deleted[dom_ins_id] = [ins_id]
        
        else:
            self.tree[self.b_id].add_dom_instruction(instruction.opcode, ins_id)

        return self.tree[self.b_id].append(ins_id)

    def add_inst_without_cse(self, ins_id):
        return self.tree[self.b_id].append_inst_without_cse(ins_id)

    def add_inst_bb(self, ins_id, b_id):
        self.tree[b_id].append(ins_id)

    def add_const_instruction(self, ins_id):
        return self.tree[self.init_bid].append_const(ins_id)

   #  can make it efficient: start bid and end bid
    def update_xold(self, var, join_bid, xold, xnew):
        node = [join_bid]
        visited = {}

        while node:
            id = node.pop()
            node = node + self.tree[id].next
            if id not in visited:
                visited[id] = True
                self.tree[id].update_xold(var, xold, xnew)

# Todo
    def remove_last_empty_bb(self):
        bb =  self.tree[self.b_id]

        # if not bb.table:
        #     for i in bb.prev:
        #         if i in self.tree:
        #             self.tree[i].next.remove(bb.id)
        #         # function call. another cfg
        #         else:
        #             bb.call_foo.tree[bb.call_foo.b_id].next.remove(bb.id)
            
        #     self.b_id= self.b_id-1

    def generate_dot(self):
        id = self.init_bid
        node = ""
        edge = ""
        
        self.rendered = True

        while id <= self.b_id:
            bb =  self.tree[id]
            node = node + "\t\t"+bb.dot_node() + "\n"
            edge = edge + "\t\t"+bb.dot_edge()
            id =id + 1

        edge = "\nsubgraph cluster_"+self.name+"{\n\tlabel="+self.name+"\n\t"+edge+"\n}" 
        return node, edge

    
    def live_variable_analysis(self):
        visited = {} # -1 for skipping the const block
        bid_list = []
        visited[self.b_id] = True
        self.tree[self.b_id].add_live_var_set(set()) # this is last statement, no live var
        prev_live_set = self.tree[self.b_id].live_variable_analysis()
        phi_x_operand_set= self.tree[self.b_id].get_phi_x_operand_set()
        phi_y_operand_set = self.tree[self.b_id].get_phi_y_operand_set()
        bid_list.extend(self.tree[self.b_id].get_parent())
        id = bid_list.pop()

        while id > self.init_bid:
            self.tree[id].add_live_var_set(prev_live_set)
            prev_live_set = self.tree[id].live_variable_analysis()

            if id not in visited:
                visited[id] = True
                bid_list.extend(self.tree[id].get_parent())
            
            if bid_list:
                parent= id
                id = bid_list.pop()
                if self.tree[id].phi_direction == X_OPERAND_BB:
                    phi_x_operand_set = self.tree[parent].get_phi_x_operand_set()
                    prev_live_set = prev_live_set.union(phi_x_operand_set)
                
                elif self.tree[id].phi_direction == Y_OPERAND_BB:
                    phi_y_operand_set = self.tree[parent].get_phi_y_operand_set()
                    prev_live_set = prev_live_set.union(phi_y_operand_set)

            else:
                break

    

relOp_fall = {EQOP:"bne", NOTEQOP: "beq", GTOP:"ble", GEQOP:"blt", LTOP:"bge", LEQOP:"bgt"}
default_foo = {"InputNum": "read", "OutputNum":"write", "OutputNewLine":"writeNL"}
cfg = None
ins_array = {}
'''
    Reference instruction map
    {
        <instrucntion id>: [inst1, inst2,...]
    }
'''
ins_ref_list = {} 
pseudo_ins = {}
pc = 0
neg_pc = -1
phi= {}
phi_x = True
phi_i=-1
current_bid = 0
cfg_list=[]
ins_array[neg_pc] = instruction(neg_pc, "const", 4, None)

def instantiate_main_CFG():
    global cfg
    cfg = CFG(current_bid)
    cfg.name = "main"
    cfg_list.append(cfg)
    cfg.add_const_instruction(neg_pc)
    return cfg

def render_dot():
    node = ""
    edge = ""

    for cfg in cfg_list:
        n, e = cfg.generate_dot()
        node = node + "\t"+n
        edge = edge + "\t"+e

    graph = "digraph G{\n" + node+ edge + "\n}"

    with open("graph.dot", "w") as f:
        f.write(graph)

def get_pc():
    return pc

def get_bid():
    return cfg.get_bid()

def get_max_bid():
    return max(cfg.tree.keys())

def set_phix(val):
    global phi_x 
    phi_x = val

def update_var_usage(identifier, ins_id):
    cfg.tree[get_bid()]

# For if statement
# Todo: copy dom instructions from dominating block
def create_join_bb(bid, var_stat):
    global phi_i
    join_bb = BB(bid) 
    join_bb.var_stat = dict(var_stat)# VAR STATE?
    phi_i = phi_i + 1
    phi[phi_i] = join_bb
    # join_bb.id = IF_JOIN_BB

# remove phi instruction for which operands are equal, x==y
# Todo: remove other outer block phi that depend's on this phi.
def remove_phi_x_eq_y(join_bb):
    inst_table = join_bb.table
    phi = join_bb.phi

    for var in list(phi.keys()):
        ins_id  = phi[var]
        inst = ins_array[ins_id]

        if inst.x == inst.y:
            # first update variable state
            join_bb.update_var(var, inst.x)
            join_bb.remove_var_usage(var, ins_id)
            inst_table.remove(ins_id)
            del phi[var]
        
# work with if statement
'''
    1. Remove phi with x == y
    2. Find the id for join bb
    3. 
'''
def add_join_bb(left, right, jump_ins):
    cfg.tree[left].phi_direction = X_OPERAND_BB
    cfg.tree[righ].phi_direction= Y_OPERAND_BB 
    join_bb = top_phi()
    remove_phi_x_eq_y(join_bb)
    join_bb.id = max(left, right) + 1
    cfg.b_id = join_bb.id
    join_bb.dom_block.append(cfg.tree[left].dom_block[-1]) # dominating block of if will be the dominating block of join block

    # if there is else block, then add bra instruction
    # to the if block
    if right - left > 1 or cfg.tree[right].table:
        inc_pc()
        ins_array[pc] = instruction(pc, "bra", join_bb.table[0], None)
        cfg.tree[left].table.append(pc)

    cfg.add_join_bb(join_bb, left, "fall-through")
    jump_to = -1

    if cfg.tree[right].table:
        jump_to = max(cfg.tree[right].table)
    elif join_bb.table:
        jump_to = min(join_bb.table)
    
    else:   
        jump_to = add_nop(join_bb.id)

    ins_array[jump_ins].update_y(jump_to)
    cfg.add_join_bb(join_bb, right, "branch")

def insert_join_bb_while():
    global phi_i
    join_bb = cfg.tree[cfg.b_id]
    phi_i = phi_i + 1
    phi[phi_i] = join_bb

def link_up_while(join_bid, jump_ins):
    # No need to add a branch to an empty block
    # if cfg.tree[cfg.b_id].is_empty():
    #     ins_array

    # else:

    # Todo:can be done easily just by checking brnach type
    cfg.tree[join_bid-1].phi_direction = X_OPERAND_BB
    cfg.tree[get_bid()].phi_direction = Y_OPERAND_BB
    inc_pc()
    ins_array[pc] = instruction(pc, "bra", cfg.tree[join_bid].table[0], None)
    cfg.add_inst_without_cse(pc)
    cfg.add_bb_man(join_bid, get_bid(), "branch")
    ins_array[jump_ins].update_y(pc+1)
    cfg.tree[cfg.b_id].delete_marked_instruction()
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

def add_nop(b_id):
    if not cfg.tree[b_id].table:
        inc_pc()
        ins_array[pc] = instruction(pc, "nop", None, None)
        cfg.tree[cfg.b_id].add_nop(pc)

        return pc

def compute(opcode, x, y):
    if x.val is None:
        return None
    
    if y.val is None:
        return None

    if opcode == ADDOP:
        x.val = x.val + y.val

    elif opcode == SUBOP:
        x.val = x.val - y.val

    elif opcode == MULOP:
        x.val = x.val * y.val

    elif opcode == DIVIDEOP:
        x.val = x.val / y.val

    return x.val
    
def code_assignment(lsymbol, rsymbol):
    # is there any case where xold is not in the dictionary
    identifier = lsymbol.name
    ins_id = 0
    xold = cfg.get_var_pointer(identifier)

    if rsymbol.kind == ARRAY:
        ins_id = rsymbol.idx[rsymbol.temp]
    
    else:
        ins_id = rsymbol.addr

    if lsymbol.kind == ARRAY:
        cfg.update_array(identifier, lsymbol.temp, ins_id)
        xold = lsymbol.idx[lsymbol.temp]

    else:
        lsymbol.addr = ins_id
        cfg.update_var(identifier, ins_id)

    temp =0
    i = phi_i

    while i > -1: 
        join_bb = phi[i]
        i = i -1
        if identifier not in join_bb.phi:
            inc_pc()
            temp = pc
            ins_array[pc] = instruction(pc, "phi", xold, xold)
            join_bb.phi[identifier] = pc
            join_bb.append_phi(pc)
            join_bb.update_var(identifier, pc)

            # update all uses of xold by phi
            if join_bb.id != IF_JOIN_BB_ID:
                cfg.update_xold(identifier,join_bb.id, xold, pc)
        
        else:
            temp = join_bb.phi[identifier]
        
        # left operand or right operand
        if phi_x:
            ins_array[temp].update_x(ins_id)
        
        else:
            ins_array[temp].update_y(ins_id)

        ins_id = pc

    return

def code_constant(val):
    dec_neg_pc()
    ins_array[neg_pc] = instruction(neg_pc, "const #", val, None)

    return cfg.add_const_instruction(neg_pc)

def code_func_call(name, arg_list):
    # Todo: parameter and argument length checking.
    if name in default_foo:
        name = default_foo[name]
        inc_pc()
        addr = None
        if name == "write":
            addr = arg_list[0]
        
        ins_array[pc] = instruction(pc, name, addr, None)
        cfg.add_inst_without_cse(pc)

    else:
        code_func_argument(arg_list)
        inc_pc()
        inst = instruction(pc, "jsr", name, None, FUNCTION)
        ins_array[pc] = inst
        cfg.add_inst_without_cse(pc)

    return pc

def code_func_parameter(param_list):
    for param in param_list:
        inc_pc()
        ins_array[pc] = instruction(pc, "par", param, None)
        cfg.add_inst_without_cse(pc)
        return

def code_func_argument(args_list):
    for arg in args_list:
        inc_pc()
        ins_array[pc] = instruction(pc, "arg", arg, None)
        cfg.add_inst_without_cse(pc)
        return 
        
def code_f2(opcode, x, y):
    inc_pc()
    if x.kind == ARRAY:
        addr1 = code_array_load(x)
    
    else:
        addr1 = x.addr

    if y.kind == ARRAY:
        addr2 = code_array_load(y)
    
    else:
        addr2 = y.addr

    ins_array[pc] = instruction(pc, opcode, addr1, addr2)
    ins_id = cfg.add_instruction(pc)

    # instruction added, no cse. update new var usage
    if ins_id == pc:
        cfg.update_var_usage(x.name, pc)
        cfg.update_var_usage(y.name, pc)

    return ins_id

def code_else(prev_bb):
    bb = cfg.create_bb()
    bb.var_stat = dict(cfg.tree[prev_bb].var_stat)
    bb.dom_block.append(prev_bb)
    cfg.add_bb_man(bb.id, prev_bb, "branch")
    return bb.id

def code_relation(resL, resR, relOp):
    inc_pc()
    cfg.update_var_usage(resL.name, pc)
    cfg.update_var_usage(resR.name, pc)

    ins_array[pc] = instruction(pc, "cmp", resL.addr, resR.addr)
    cfg.add_instruction(pc)
    inc_pc()
    ins = instruction(pc, relOp_fall[relOp], pc-1, "follow")
    ins_array[pc] = ins
    cfg.add_inst_without_cse(pc)   
    return pc

def code_array_offset(avar):
    inc_pc()
    ins_array[pc] = instruction(pc, "mul", avar.temp, INT_SIZE_INS)
    addr1 = cfg.add_instruction(pc)
    inc_pc()
    ins_array[pc] = instruction(pc, "addi", BP, avar.base)
    addr2 = cfg.add_instruction(pc)
    inc_pc()
    ins_array[pc] = instruction(pc, "adda", addr1, addr2)
    cfg.add_inst_without_cse(pc) # pc will be added with guarantee and will not be replaced by previous ins_id.

    return pc

def code_kill(avar):
    if phi:
        join_bb = top_phi()
        inc_pc()
        ins_array[pc] = instruction(pc, "kill", avar.name, None)
        join_bb.append(pc)

        avar.idx = {}
        return

def code_array_store(avar, res):
    code_kill(avar)
    addr = code_array_offset(avar)
    inc_pc()
    addr2 = 0
    if res.kind == ARRAY:
        addr2 = res.idx[res.temp]
    
    else:
        addr2 = res.addr

    avar.idx[avar.temp] = addr2 # update the array symbol's idx
    ins_array[pc] = instruction(pc, "store", addr, addr2)
    cfg.add_inst_without_cse(pc)

    return avar

def code_array_load(avar):
    # avoid duplicate load
    if avar.temp in avar.idx:
        return avar.idx[avar.temp]
        
    addr = code_array_offset(avar)
    inc_pc()
    ins_array[pc] = instruction(pc, "load", addr, None)
    cfg.add_instruction(pc)

    return pc

def code_return():
    inc_pc()
    ins_array[pc] = instruction(pc, "ret", None, None)
    cfg.add_inst_without_cse(pc)

def code_end():
    inc_pc()
    ins_array[pc] = instruction(pc, "end", None, None)
    cfg.add_inst_without_cse(pc)