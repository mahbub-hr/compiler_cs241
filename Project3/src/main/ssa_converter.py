from code_generator import ins_array

class reg_instruction:
    def __init__(self, ins, register_allocation):
        self.opcode = self.opcode(ins)


        self.r1 = self.get_r1(register_allocation)

        self.r2 = register_allocation[ins.y]
        self.r3 = ins_array[ins.x].x
        
        if ins.y < 0:
            self.r2 = register_allocation[ins.x]
            self.r3 = ins_array[ins.y].x

    def opcode(self, ins):
        if ins.x is not None and ins.y is not None and  (ins.x <0 or ins.y < 0):
            return ins.opcode+"i"
        
        return ins.opcode

    def get_r1(ins, register_allocation):
        if ins.opcode ==  "write":
            return register_allocation[ins.x]

        return register_allocation[ins.ins_id]

    def __str__(self):
        string = f"{self.opcode} {self.r1}, {self.r2}, {self.r3}"
        return string

     