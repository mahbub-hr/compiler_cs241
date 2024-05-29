from asmpl.core import Constant, code_generator
from asmpl.wasm import reg_to_wasm 

def get_const_val(x):
        return code_generator.ins_array[x].x

class reg_instruction:
    ins_array = code_generator.ins_array

    def __init__(self):
        self.opcode = ""
        self.r1 = -1
        self.r2 = -1
        self.r3 = -1   
        self.string = None


    def check_x(reg_ins, register_allocation, x):
        regtowasm = reg_to_wasm.get_reg_to_stack()
        if x < 0:
            regtowasm.push_constant(get_const_val(x))
            reg_ins.string = f"push #{get_const_val(x)}"

        else:
            regtowasm.push_variable(register_allocation[x])
            reg_ins.string = f"push R{register_allocation[x]}"
        
        return reg_ins

    def check_xy(reg_ins, register_allocation, x, y):
        regtowasm = reg_to_wasm.get_reg_to_stack()
        ins_array = code_generator.ins_array
        if x > 0:
            rx = register_allocation[x]
            reg_ins.r2 = rx
            regtowasm.push_variable(rx)
            reg_ins.string = f"push R{rx}, "
            if y > 0:
                ry = register_allocation[y]
                reg_ins.r3 = ry
                regtowasm.push_variable(ry)
                reg_ins.string = reg_ins.string + f"push R{ry}"
            else:
                const_y = ins_array[y].x
                reg_ins.r3 = const_y
                regtowasm.push_constant(const_y)
                reg_ins.string = reg_ins.string + f"push #{const_y}"
        else:
            const_x = ins_array[x].x
            reg_ins.r3 = const_x
            regtowasm.push_constant(const_x)
            reg_ins.string =  f"push #{const_x}, "
            if y > 0:
                ry = register_allocation[x]
                reg_ins.r2 = ry
                regtowasm.push_variable(ry)
                reg_ins.string = reg_ins.string + f"push R{ry}"
            else:
                const_y = ins_array[y].x
                reg_ins.r3 = const_y
                regtowasm.push_constant(const_y)
                reg_ins.string = reg_ins.string + f"push #{const_y}\n"

        return reg_ins


    def create_ins(ins, register_allocation, bb:code_generator.BB):
        reg_to_stack = reg_to_wasm.get_reg_to_stack()
        ins_array = code_generator.ins_array
        # for while branch block
        if ins.opcode == "phi":
            b_op = -1
            b_ssa = ins.y

            if b_ssa < 0:
                b_op = ins_array[b_ssa].x 

            else:
                b_op = register_allocation[b_ssa]

            reg_ins = reg_instruction.create_move_ins(ins.ins_id, b_op)
            reg_ins.string = f"{reg_ins.opcode} R{reg_ins.r1}, R{reg_ins.r2}"
            return reg_ins

        reg_ins = reg_instruction()

        # end
        if ins.opcode == "end":
            reg_to_stack.add_instruction("end")
            reg_ins.string = "end"
            return reg_ins

        if ins.opcode == "nop":
            reg_ins.string = ins.opcode
            return reg_ins

        if ins.opcode == "writeNL":
            reg_ins.string = "writeNL"
            return reg_ins

        if ins.opcode == "kill":
            reg_ins.string = f"{ins.opcode} {ins.x}"
            return reg_ins

        if ins.opcode == "jsr":
            reg_to_stack.call_function(ins.x)
            reg_ins.string = f"{ins.opcode} {ins.x}"
            return reg_ins
        
        if ins.opcode == "ret":
            if ins.x:
                reg_instruction.check_x(reg_ins, register_allocation, ins.x)
            
            else:
                reg_ins.string = "ret"

            reg_to_stack.add_instruction("ret")
            return reg_ins

        if ins.opcode == "retval":
            reg_ins = reg_instruction.create_move_ins(register_allocation[ins.ins_id], 31)
            reg_to_stack.save_to_reg(register_allocation[ins.ins_id])
            reg_ins.string = f"pop R{register_allocation[ins.ins_id]}"
            return reg_ins
        
        if ins.opcode == Constant.ASSIGN_OPCODE:
            reg_ins.string = str(ins)
            return reg_ins

        reg_ins.opcode = reg_instruction.opcode(ins)
        # 1 reg ins
        if ins.opcode == "read":
            reg_to_stack.input(ins.ins_id)
            reg_ins.string= f"{reg_ins.opcode} R{register_allocation[ins.ins_id]}"
            return reg_ins

        if ins.opcode == "par":
            r = register_allocation[ins.ins_id]
            reg_to_stack.create_or_get_wasm_variable(r)
            reg_ins.string= f"{reg_ins.opcode} R{r}"
            return reg_ins

        if ins.opcode == "arg":
            reg_ins = reg_instruction.check_x(reg_ins, register_allocation, ins.x)
            
            return reg_ins

        if ins.opcode == "write":
            reg_instruction.check_x(reg_ins, register_allocation, ins.x)
            reg_to_stack.add_print_instruction()
            return reg_ins

        elif ins.opcode in Constant.BRANCH_OPCODE:
            # bra(7)
            if ins.opcode == "bra":
                if bb.is_id_greater_than_parent():
                    '''WHILE branch'''
                    reg_to_stack.add_label_instruction("bra", 0)
                    reg_to_stack.add_instruction("end")
                    reg_to_stack.add_instruction("end")
            
            if bb.join_type == Constant.WHILE_JOIN_BLOCK:
                reg_to_stack.add_instruction(ins.opcode)
                reg_to_stack.add_label_instruction("bra_if", 1)

            else:
                reg_to_stack.add_instruction(ins.opcode)

            reg_ins.string = f"{reg_ins.opcode} {reg_ins.r1}"
            return reg_ins

        # 2 register instruciton
        elif ins.opcode=="cmp":
            reg_instruction.check_xy(reg_ins, register_allocation, ins.x, ins.y)
            return reg_ins

        # only for addi bp a_base
        elif ins.opcode=="addi":
            reg_ins.string = f"{ins.opcode} R{Constant.BP_REG} R{ins.y}"
            return reg_ins

        elif ins.opcode == "store":
            op = 0
            if ins.y<0:
                op = ins_array[ins.y].x

            else:
                op = ins.y

            reg_ins.string = f"{ins.opcode} Mem[R{register_allocation[ins.x]}], R{op}"
            return reg_ins

        elif ins.opcode == "load":
            reg_ins.string = f"{ins.opcode} R{register_allocation[ins.ins_id]}, Mem[R{register_allocation[ins.x]}]"
            return reg_ins

        elif ins.opcode == "move":
            reg_ins = reg_instruction.check_x(reg_ins, register_allocation, ins.y)
            reg_to_stack.save_to_reg(register_allocation[ins.x])
            reg_ins.string  = reg_ins.string + f", pop R{register_allocation[ins.x]}"
            return reg_ins

        # 3 regiter instruction
        reg_ins.r1 = register_allocation[ins.ins_id]
        
        # load Constant value
        
        reg_instruction.check_xy(reg_ins, register_allocation, ins.x, ins.y)
        
        reg_to_stack.add_instruction(reg_ins.opcode)
        reg_to_stack.save_to_reg(reg_ins.r1)
        reg_ins.string = reg_ins.string + f", {ins.opcode} R{reg_ins.r1}"
        return reg_ins

    def opcode(ins):
        if "i" in ins.opcode:
            return ins.opcode[:-1]

        if ins.x is not None and ins.y is not None and  (ins.x <0 or ins.y < 0):
            return ins.opcode
        
        return ins.opcode


    def create_move_ins(op1, op2):
        move_ins = reg_instruction()
        move_ins.opcode = "move"
        move_ins.r1 = op1
        move_ins.r2 = op2
        move_ins.string=f"move R{move_ins.r1}, R{move_ins.r2}"
        return move_ins

    def find_branch_instruction_idx(b_parent):
        idx= len(b_parent.table)-1
        # if ins_array[idx].opcode in Constant.BRACH_OPCODE:
        #     return idx

        return -1

    def convert_IF_phi_instruction(phi_ins, b_parent, f_parent, b_ssa, f_ssa, register_allocation):
        b_op=-1
        f_op =-1
        ins_array = code_generator.ins_array

        if b_ssa < 0:
            b_op = ins_array[b_ssa].x 

        else:
            b_op = register_allocation[b_ssa]

        if f_ssa < 0:
            f_op = ins_array[f_ssa].x 

        else:
            f_op = register_allocation[f_ssa]

        b_parent_move_ins = reg_instruction.create_move_ins(register_allocation[phi_ins.ins_id], b_op) 
        f_parent_move_ins = reg_instruction.create_move_ins(register_allocation[phi_ins.ins_id], f_op)
        b_ins =code_generator.instruction.create_instruction("move", phi_ins.ins_id, phi_ins.x)
        f_ins = code_generator.instruction.create_instruction("move", phi_ins.ins_id, phi_ins.y)

        b_parent_b_ins_idx = reg_instruction.find_branch_instruction_idx(b_parent)

        b_parent.table.insert(b_parent_b_ins_idx, b_ins.ins_id)
        b_parent.reg_instruction.insert(b_parent_b_ins_idx, b_parent_move_ins)
        
        f_parent.table.append(f_ins.ins_id)
        f_parent.reg_instruction.append(f_parent_move_ins)
        
        return

    def convert_WHILE_phi_instruction(ins, b_parent, f_parent, register_allocation):
        f_op =-1
        f_ssa = ins.x
        ins_array = code_generator.ins_array
        
        if f_ssa < 0:
            f_op = ins_array[f_ssa].x 

        else:
            f_op = register_allocation[f_ssa]

        f_parent_move_ins = reg_instruction.create_move_ins(register_allocation[ins.ins_id], f_op)
        
        f_ins = code_generator.instruction.create_instruction("move", ins.ins_id, ins.x)
        f_parent.table.append(f_ins.ins_id)
        f_parent.reg_instruction.append(f_parent_move_ins)

        b_ins =code_generator.instruction.create_instruction("move", ins.ins_id, ins.y)
        b_parent_b_ins_idx = reg_instruction.find_branch_instruction_idx(b_parent)
        # for later use
        b_parent.table.insert(b_parent_b_ins_idx, b_ins.ins_id)

        return


    def __str__(self):
        # r3 = ""
        # r2 = ""

        # if self.r2 != -1:
        #     r2 = f"R{self.r2}, "

        # if self.r3 != -1:
        #     r3 = f"R{self.r3}"

        # if self.val:
        #     r3 = val

        # string = f"{self.opcode} R{self.r1}, {r2} {r3}"
        return self.string

     