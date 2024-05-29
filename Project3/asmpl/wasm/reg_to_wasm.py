import sys
from asmpl.wasm.emitter import Emitter
from asmpl.wasm.format import Types, Opcodes, MAP_SSA_TO_WASM
from asmpl.core import symbol_table, code_generator, file, Constant

class WasmFunc:
    def __init__(self, name, index=0):
        self.name = name
        self.index = index
        self.local_type = {}
        self.params =[]
        self.fetched_param_idx = -1
        self.results = []
        self.body = bytearray()

    def add_param(self, _type:list):
        self.params = _type
        return 

    # def get_param(self):
    #     '''Subsequent call to this function fetch the next parameter in the list'''
    #     self.fetched_param_idx = self.fetched_param_idx + 1
        
    #     if self.fetched_param_idx >= len(self.params):
    #         sys.exit("Get call on param exceeds the number of parameters")

    #     self.add_instruction(bytearray([Opcodes.get_local.value, self.fetched_param_idx]))

    #     return 

    def add_local(self, _type:Types.i32.value):
        if _type not in self.local_type:
            self.local_type[_type] = 0

        self.local_type[_type] = self.local_type[_type] + 1

        return

    def add_result(self, _type:list):
        self.results= _type

    def add_instruction(self, instruciton:bytearray):
        self.body.extend(instruciton)
        
    def to_byte_array(self):
        buffer = bytearray()

        for _type in self.local_type:
            buffer.append(self.local_type[_type])
            buffer.append(_type)

        buffer = bytearray([len(self.local_type)]) + buffer + self.body

        return buffer
        
class RegToStackMachineCode:
    def __init__(self):
        self.emitter = Emitter()
        self.emitter.init_import_section()
        '''func_name : idx'''
        self.func_type_idx = {}

    def export_main_func(self):
        self.emitter.init_export_section(self.emitter.get_num_of_types())

        return 

    def add_local_func(self, name, params:list, returns):
        self.func_type_idx[name] = self.emitter.get_num_of_types()

        if name == Constant.MAIN_FUNC_NAME:
            self.export_main_func()

        self.cur_function = WasmFunc(name, self.emitter.get_num_of_types())
        self.cur_function.add_param([Types.i32.value]*len(params))
        result = []
        if returns:
            result.append(Types.i32.value)

        self.cur_function.add_result(result)
        self.reg_to_var = {}
        self.cur_var_idx = 0

        return self.cur_function

    def append_func_to_module(self):
        emitter = self.emitter
        func = self.cur_function
        func.add_instruction(bytearray([Opcodes.end.value]))


        emitter.add_function_type(func.params, func.results)
        emitter.add_func()
        emitter.add_func_body(func.to_byte_array())

    def add_instruction(self, opcode:str):
        if opcode == "bra":#ignore
            return 

        opcode = MAP_SSA_TO_WASM[opcode]
        self.cur_function.add_instruction(bytearray([opcode.value]))

        return

    def add_label_instruction(self, opcode:str, label):
        opcode = MAP_SSA_TO_WASM[opcode]
        self.cur_function.add_instruction(bytearray([opcode.value, label]))
        return 

    def call_function(self, func_name):
        func_idx = self.func_type_idx[func_name]
        self.cur_function.add_instruction(bytearray([Opcodes.call.value, func_idx]))

        return 

    def add_print_instruction(self):
        buffer = bytearray([Opcodes.call.value, Emitter.LOG_FUNC_IDX])
        self.cur_function.add_instruction(buffer)
        return buffer

    def push_constant(self, const:int):
        arr = bytearray([Opcodes.i32_const.value, const]) 
        self.cur_function.add_instruction(arr)
    
    def push_variable(self, reg_no):
        import sys
        '''load the value of reg_no and push to the stack'''
        if reg_no not in self.reg_to_var:
            sys.exit(f"No {reg_no} found in the map")

        var_idx = self.reg_to_var[reg_no]

        self.cur_function.add_instruction(bytearray([Opcodes.get_local.value, var_idx]))
    
    def input(self, reg_no):
        self.cur_function.remove_last_instruction()
        return

    def create_or_get_wasm_variable(self, reg_no):
        '''Map reg_no --> wasm var_idx. Does not set the var.'''
        if reg_no in self.reg_to_var:
            return self.reg_to_var[reg_no]

        self.reg_to_var[reg_no] = self.cur_var_idx
        self.cur_function.add_local(Types.i32.value)
        self.cur_var_idx = self.cur_var_idx + 1

        return self.cur_var_idx-1

    def set_variable(self, var_idx):
        self.cur_function.add_instruction(bytearray([Opcodes.set_local.value, var_idx]))

        return

    def save_to_reg(self, reg_no):
        '''save the top of the stack to reg_no --> var_idx''' 
        var_idx = self.create_or_get_wasm_variable(reg_no)
        self.set_variable(var_idx)

        return


    def write_to_file(self):
        buffer = self.emitter.encode_module()
        self.emitter.write_to_file(file.get_wasm_file_path(), buffer)

    
reg_to_stack = None
def get_reg_to_stack():
    global reg_to_stack

    if reg_to_stack:
        return reg_to_stack

    reg_to_stack = RegToStackMachineCode()
    return reg_to_stack