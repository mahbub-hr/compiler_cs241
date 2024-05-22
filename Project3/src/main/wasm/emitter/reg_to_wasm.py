from emitter import Emitter
from format import Types


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

    def add_instruction(self, ):

class RegToWASM:
    def __init__(self):
        self.emitter = Emitter()
        self.emitter.init_import_section()
        self.emitter.export_section()

    def add_local_func(self, params: list, results: list, local_decl_count, body):
        self.emitter.add_function_type(params, results)
        self.emitter.add_func()
        self.emitter.add_func_body(local_decl_count, body)

    def add_local_var(self, )