from code_generator import ins_array
import Constant
class reg_instruction:
    def __init__(self):
        self.opcode = ""
        self.r1 = -1
        self.r2 = -1
        self.r3 = -1   
        self.string = None

    def create_ins(ins, register_allocation):
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
        if ins.opcode in ["end", "nop"]:
            reg_ins.string = ins.opcode
            return reg_ins

        if ins.opcode == "writeNL":
            reg_ins.string = "writeNL"
            return reg_ins

        if ins.opcode in ["jsr", "kill"]:
            reg_ins.string = f"{ins.opcode} {ins.x}"
            return reg_ins
        
        if ins.opcode == "ret":
            if ins.x <0:
                reg_ins.string = f"movei R31, {ins_array[ins.x].x}\nret"
                return reg_ins

            elif ins.x:
                reg_ins.string = f"move R31, R{register_allocation[ins.x]}\nret"
                return reg_ins
            else:
                reg_ins.string = "ret"
                return reg_ins

        if ins.opcode == "retval":
            reg_ins = reg_instruction.create_move_ins(register_allocation[ins.ins_id], 31)
            return reg_ins
        
        if ins.opcode == Constant.ASSIGN_OPCODE:
            reg_ins.string = str(ins)
            return reg_ins

        reg_ins.opcode = reg_instruction.opcode(ins)
        # 1 reg ins
        if ins.opcode in ["read", "par"]:
            reg_ins.string= f"{reg_ins.opcode} R{register_allocation[ins.ins_id]}"
            return reg_ins

        if ins.opcode == "arg":
            if ins.x <0:
                reg_ins.string = f"movei R{register_allocation[ins.ins_id]}, {ins_array[ins.x].x}"
                return reg_ins

            else:
                reg_ins.string = f"move R{register_allocation[ins.ins_id]}, R{register_allocation[ins.x]}"
                return reg_ins

        if ins.opcode == "write":
            op = 0
            if ins.x < 0:
                reg_ins.string = f"{reg_ins.opcode} {ins_array[ins.x].x}"
            
            else:
                reg_ins.string = f"{reg_ins.opcode} R{register_allocation[ins.x]}"
 
            return reg_ins

        elif ins.opcode in Constant.BRACH_OPCODE:
            # bra(7)
            if ins.y is None:
                reg_ins.r1 = ins.x
            else:
                reg_ins.r1 = ins.y

            reg_ins.string = f"{reg_ins.opcode} {reg_ins.r1}"
            return reg_ins

        # 2 register instruciton
        elif ins.opcode=="cmp":
            if ins.x < 0 and ins.y < 0:
                reg_ins.string = f"{reg_ins.opcode} {ins_array[ins.y].x}, {ins_array[ins.x].x}"

            elif ins.x < 0:
                reg_ins.string = f"{reg_ins.opcode} R{register_allocation[ins.y]}, {ins_array[ins.x].x}"
            
            elif ins.y < 0:
                reg_ins.string=f"{reg_ins.opcode} R{register_allocation[ins.x]}, {ins_array[ins.y].x}" 

            else:
                reg_ins.string=f"{reg_ins.opcode} R{register_allocation[ins.x]}, {register_allocation[ins.y]}"

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

        # 3 regiter instruction
        reg_ins.r1 = register_allocation[ins.ins_id]
        
        # load Constant value
        if ins.x is not None and ins.x < 0:
            reg_ins.r3 = ins_array[ins.x].x 

        elif ins.y is not None and ins.y < 0:    
            reg_ins.r3 = ins_array[ins.y].x
            
        else:
            reg_ins.r2 = register_allocation[ins.x]
            reg_ins.r3 = "R" + str(register_allocation[ins.y])
            
        reg_ins.string = f"{reg_ins.opcode} R{reg_ins.r1}, R{reg_ins.r2}, {reg_ins.r3}"
        return reg_ins

    def opcode(ins):
        if "i" in ins.opcode:
            return ins.opcode

        if ins.x is not None and ins.y is not None and  (ins.x <0 or ins.y < 0):
            return ins.opcode+"i"
        
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

        b_parent_b_ins_idx = reg_instruction.find_branch_instruction_idx(b_parent)

        b_parent.table.insert(b_parent_b_ins_idx, phi_ins.ins_id)
        b_parent.reg_instruction.insert(b_parent_b_ins_idx, b_parent_move_ins)
        
        f_parent.table.append(phi_ins.ins_id)
        f_parent.reg_instruction.append(f_parent_move_ins)
        
        return

    def convert_WHILE_phi_instruction(ins, b_parent, f_parent, register_allocation):
        f_op =-1
        f_ssa = ins.x

        if f_ssa < 0:
            f_op = ins_array[f_ssa].x 

        else:
            f_op = register_allocation[f_ssa]

        f_parent_move_ins = reg_instruction.create_move_ins(register_allocation[ins.ins_id], f_op)
        f_parent.table.append(ins.ins_id)
        f_parent.reg_instruction.append(f_parent_move_ins)

        b_parent_b_ins_idx = reg_instruction.find_branch_instruction_idx(b_parent)
        # for later use
        b_parent.table.insert(b_parent_b_ins_idx, ins.ins_id)

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

     