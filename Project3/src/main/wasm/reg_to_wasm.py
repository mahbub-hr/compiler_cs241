from .emitter import Emitter
from .format import Types, Opcodes, MAP_SSA_TO_WASM
import symbol_table
import code_generator
import Constant

class WasmFunc:
    def __init__(self, name, index=0):
        self.index = index
        self.local_type = {}
        self.param =[]
        self.result = []
        self.body = bytearray()

    def add_param(self, _type:list):
        self.param = _type
        return 

    def add_local(self, _type:Types.i32):
        if _type not in self.local_type:
            self.local_type[_type] = 0

        self.local_type[_type] = self.local_type[_type] + 1

        return

    def add_result(self, _type:list):
        self.result= _type

    def add_instruction(self, instruciton:bytearray):
        self.body.extend(instruciton)


class RegToStackMachineCode:
    def __init__(self):
        self.emitter = Emitter()
        self.emitter.init_import_section()
        self.emitter.init_export_section()

    def add_local_func(self):
        self.emitter.add_func()
        self.cur_function = WasmFunc()
        self.reg_to_var = {}
        self.cur_var_idx = 0

    def add_instruction(self, opcode):
        
        opcode = MAP_SSA_TO_WASM[opcode].value
        self.cur_function.add_instruction(bytearray[opcode])

        return

    def add_print_instruction(self):
        self.cur_function.add_instruction(bytearray([Opcodes.call, ]))
        return

    def push_constant(self, const):
        self.cur_function.add_instruction(bytearray([Opcodes.i32_const, const]))
    
    def push_variable(self, reg_no):
        if(var_idx < Constant.NO_OF_GPR):
            '''already in the stack'''
            return

        var_idx = self.create_wasm_variable(reg_no)
        self.cur_function.add_instruction(bytearray([Opcodes.get_local, var_idx]))
    
    def create_wasm_variable(self, reg_no):
        if reg_no in self.reg_to_var:
            return self.reg_to_var[reg_no]

        self.reg_to_var[reg_no] = self.cur_var_idx
        self.cur_function.add_local(Types.i32.value)
        self.cur_var_idx = self.cur_var_idx + 1

        return self.cur_var_idx-1
    
reg_to_stack = None
def get_reg_to_stack():
    global reg_to_stack

    if reg_to_stack:
        return reg_to_stack

    reg_to_stack = RegToStackMachineCode()
    return reg_to_stack