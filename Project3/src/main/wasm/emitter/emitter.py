from format import Section, Opcodes, TypeSectionFormat

class Emitter:
    WASM_BINARY_MAGIC = bytearray(b'\x00\61\x73\x6d')
    WASM_BINARY_VERSION = bytearray(b'\x01\x00\x00\x00')

    def __init__(self):
        self.buffer = bytearray()
        self.num_of_type = 0
        self.num_of_func = 0
        self.num_of_exp =0
        self.num_of_imp = 0
        self.num_of_code = 0

        self.type_section= bytearray()
        self.func_section = bytearray()
        self.imp_section = bytearray()
        self.exp_section = bytearray()
        self.code_section = bytearray()

        return

    def encode_header(self):
        return self.WASM_BINARY_MAGIC+self.WASM_BINARY_VERSION

    def encode_section(self, section_id):
        '''Add two bytes: section_id and section size --> 0'''
        section_buffer = bytearray([section_id.value])
        section_buffer.append(0) # section size. Need to be filled later

        return section_buffer

    def init_type_section(self):
        '''Need to compute the final size of the section later'''
        self.type_section = self.encode_section(Section._type.value)

        return self.type_section

    def init_func_section(self):
        self.func_section = self.encode_section(Section._func.value)
        return self.func_section

    def init_exp_section(self):
        self.exp_section = self.encode_section(Section._export.value)
        return self.exp_section

    def init_imp_section(self):
        self.imp_section = self.encode_section(Section._import.value)
        return self.imp_section

    def init_code_section(self):
        self.code_section = self.encode_section(Section._code.value)
        return self.code_section

    def add_type(self, type_buffer:bytearray):
        self.num_of_type = self.num_of_type + 1
        self.type_section.extend(type_buffer)

        return self.type_section

    def add_result_type(self, rt:list):
        buffer = bytearray()
        buffer.append(len(rt))
        for r in rt:
            buffer.append(r)

        return buffer

    def prepare_function_type(self, params:list, results:list ):
        buffer = bytearray()
        buffer.append(0x60)
        buffer.extend(self.add_result_type(params))
        buffer.extend(self.add_result_type(results))
        return buffer

    def add_import(self, imp_buffer:bytearray):
        self.num_of_imp = self.num_of_imp + 1 
        self.imp_section.extend(imp_buffer)

        return self.imp_section

    def prepare_import(self, module_name, field_name, imp_kind, imp_signature_idx=0):
        buffer = bytearray([len(module_name), module_name, len(field_name), field_name, imp_kind, imp_signature_idx])

        return buffer
        
    def add_func(self):
        self.func_section.append(self.num_of_func)
        self.num_of_func = self.num_of_func + 1

        return self.func_section

    def add_export(self, exp_buffer:bytearray):
        self.num_of_exp = self.num_of_exp + 1
        self.exp_section.extend(exp_buffer)

        return self.exp_section

    def prepare_export(self, exp_name, exp_kind, func_idx=0):
        buffer = bytearray([len(exp_name), exp_name, exp_kind, func_idx])
        
        return buffer
        
    def prepare_func_body(self, num_of_local, body:bytearray):
        buffer = bytearray([num_of_local]) + body
        buffer = bytearray([len(buffer)]) + buffer

        return buffer

    def encode_module(self):
        buffer = self.type_section + self.imp_section + self.func_section + self.exp_section + self.code_section
        return buffer

    def write_to_file(self, filename):
        with open(filename+".wasm", "wb") as f:
            f.write(self.buffer)
        
        return

    def print_buffer(self):
        # Print 4 bytes per line with index
        for i in range(0, len(self.buffer), 4):
            print(f"{i:04d}: {self.buffer[i:i+4]}")

        return
    