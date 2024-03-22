from code_generator import ins_array
import Constant
class reg_instruction:
    def __init__(self):
        self.opcode = ""
        self.r1 = -1
        self.r2 = -1
        self.r3 = -1   

    def create_ins(ins, register_allocation):
        reg_ins = reg_instruction()
        reg_ins.opcode = reg_instruction.opcode(ins)

        # end
        if ins.opcode == "end":
            return reg_ins

        # 1 reg ins
        if ins.opcode == "write":
            reg_ins.r1 = register_allocation[ins.x]
            return reg_ins

        elif ins.opcode in Constant.BRACH_OPCODE:
            # bra(7)
            if ins.y is None:
                reg_ins.r1 = register_allocation[ins.x]
            else:
                reg_ins.r1 = register_allocation[ins.y]

            return reg_ins

        # 2 register instruciton
        elif ins.opcode=="cmp":
            if ins.x > 0:
                reg_ins.r1 = register_allocation[ins.x]
            
            else:
                reg_ins.r1 = ins_array[ins.x].x

            if ins.y > 0:
                reg_ins.r2 = register_allocation[ins.y]

            else:
                reg_ins.r2 = ins_array[ins.y].x

            return reg_ins

        # 3 regiter instruction
        reg_ins.r1 = register_allocation[ins.ins_id]
        
        # load Constant value
        if ins.x is not None:
            if ins.x is not None and ins.x < 0:
                reg_ins.r2 = ins_array[ins.x].x 
            
            else:
                reg_ins.r2 = register_allocation[ins.x]

        if ins.y is not None:
            if ins.y < 0:    
                reg_ins.r3 = ins_array[ins.y].x
            
            else:
                reg_ins.r3 = register_allocation[ins.y]
            
        return reg_ins

    def opcode(ins):
        if ins.x is not None and ins.y is not None and  (ins.x <0 or ins.y < 0):
            return ins.opcode+"i"
        
        return ins.opcode


    def create_move_ins(op1, op2):
        move_ins = reg_instruction()
        move_ins.opcode = "move"
        move_ins.r1 = op1
        move_ins.r2 = op2
        return move_ins

    def find_branch_instruction_idx(b_parent):
        idx= len(b_parent.table)-1
        # if ins_array[idx].opcode in Constant.BRACH_OPCODE:
        #     return idx

        return -1

    def convert_phi_instruction(phi_ins, b_parent, f_parent, b_ssa, f_ssa, register_allocation):
        b_parent_move_ins = reg_instruction.create_move_ins(register_allocation[phi_ins.ins_id], register_allocation[b_ssa]) 
        f_parent_move_ins = reg_instruction.create_move_ins(register_allocation[phi_ins.ins_id], register_allocation[f_ssa])

        b_parent_b_ins_idx = reg_instruction.find_branch_instruction_idx(b_parent)

        b_parent.table.insert(b_parent_b_ins_idx, phi_ins.ins_id)
        b_parent.reg_instruction.insert(b_parent_b_ins_idx, b_parent_move_ins)
        
        f_parent.table.append(phi_ins.ins_id)
        f_parent.reg_instruction.append(f_parent_move_ins)
        
        return

    def __str__(self):
        r3 = ""
        r2 = ""

        if self.r2 != -1:
            r2 = f"R{self.r2}, "

        if self.r3 != -1:
            r3 = f"R{self.r3}"

        string = f"{self.opcode} R{self.r1}, {r2} {r3}"
        return string

     