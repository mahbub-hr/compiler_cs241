import leb128
from asmpl.wasm.format import SectionID, SectionFormat, Opcodes, Types, ExportKind

class Section:
    def __init__(self, id):
        self.id = id
        self.num_of_entry = 0
        self.buffer = bytearray()

    def get_section(self, id):
        if id == SectionID._type.value:
            return Section(id)
        
        return 

    def add_entry(self, entry_buffer:bytearray):
        self.num_of_entry = self.num_of_entry + 1
        self.buffer.extend(entry_buffer)

        return self.buffer

    def encode(self):
        '''Add two bytes: section_id and section size --> 0'''
        buffer = bytearray([self.num_of_entry])+self.buffer
        buffer = bytearray([self.id]) + leb128.u.encode(len(buffer)) + buffer
        
        return buffer

    def write_to_file(self, buffer):
        '''filename: without extension'''
        with open(f"section_{self.id}.wasm", "wb") as f:
            f.write(selfbuffer)
        return

    def validate(self):
        assert self.buffer[SectionFormat.id.value] == SectionID._code.value
        size = self.buffer[SectionFormat.size.value]
        num_of_entry = self.buffer[SectionFormat.number_of_entry.value]
        content = self.buffer[SectionFormat.cont_start.value: ]
        assert size == len(self.buffer[(SectionFormat.size.value + 1):])
        assert num_of_entry == self.num_of_entry

        return

class CodeSection(Section):
    
    def __init__(self, id):
        super().__init__(id)
        return

    def validate(self):
        
        super().validate()
        
        id = 0
        while id < num_of_entry:
            self.validate_single_function(content)

    def validate_single_function(self, content: bytearray):
        func_body_size = content[0]
        assert func_body_size == len(content[1:])
        local_decl_count = content[1]

        for i in range(0, local_decl_count):
            local_type_count = content[2]

        return 

class Emitter:
    LOG_FUNC_IDX = None
    WASM_BINARY_MAGIC = bytearray(b'\x00\x61\x73\x6d')
    WASM_BINARY_VERSION = bytearray(b'\x01\x00\x00\x00')

    def __init__(self):
        self.type_section = Section(SectionID._type.value)
        self.import_section = Section(SectionID._import.value)
        self.function_section = Section(SectionID._func.value)
        self.export_section = Section(SectionID._export.value)
        self.code_section = CodeSection(SectionID._code.value)
        
        return

    def encode_header(self):
        return self.WASM_BINARY_MAGIC+self.WASM_BINARY_VERSION

    

    # def init_type_section(self):
    #     '''Need to compute the final size of the section later'''
    #     self.type_section = self.encode_section(Section._type.value)

    #     return self.type_section

    # def init_func_section(self):
    #     self.func_section = self.encode_section(Section._func.value)
    #     return self.func_section

    def init_export_section(self, func_idx):
        """Always export a default main function"""
        self.add_export("main", ExportKind.func.value, func_idx)

        return self.export_section

    def init_import_section(self):
        self.add_import("console", "log", ExportKind.func.value)
        Emitter.LOG_FUNC_IDX = self.type_section.num_of_entry
        self.add_function_type([Types.i64.value], [])

        return self.import_section

    # def init_code_section(self):
    #     self.code_section = self.encode_section(Section._code.value)
    #     return self.code_section

    def add_result_type(self, rt:list):
        buffer = bytearray()
        buffer = buffer + leb128.u.encode(len(rt))
        for r in rt:
            buffer.append(r)

        return buffer

    def add_function_type(self, params:list, results:list ):
        '''
            params = [Types.i64.value, Types.i64.value, ..]
            results = [Types.i64.value, Types.i64.value, ..]
        '''
        buffer = bytearray()
        buffer.append(Types.func.value)
        buffer.extend(self.add_result_type(params))
        buffer.extend(self.add_result_type(results))

        self.type_section.add_entry(buffer)

        return buffer
    
    def add_import(self, module_name, field_name, imp_kind, imp_signature_idx=0):
        buffer = leb128.u.encode(len(module_name)) +  module_name.encode("utf-8")+ bytearray([len(field_name)]) + field_name.encode("utf-8")+ bytearray([imp_kind, imp_signature_idx])
        self.import_section.add_entry(buffer)

        return buffer

    def add_func(self):
        buffer = bytearray([self.type_section.num_of_entry-1])
        self.function_section.add_entry(buffer)

        return buffer

    def add_export(self, exp_name, exp_kind, func_idx=0):
        buffer = leb128.u.encode(len(exp_name))+  exp_name.encode("utf-8") + bytearray([exp_kind, func_idx])
        self.export_section.add_entry(buffer)
        return buffer
        
    def add_func_body(self, body:bytearray):
        buffer = leb128.u.encode(len(body)) + body
        self.code_section.add_entry(buffer)

        return buffer

    def encode_module(self):
        buffer = self.encode_header() + self.type_section.encode() + self.import_section.encode()+ self.function_section.encode() + self.export_section.encode() + self.code_section.encode()
        return buffer

    def write_to_file(self, filename, buffer):
        '''filename: without extension'''
        with open(filename+"test.wasm", "wb") as f:
            f.write(buffer)
        
        return

    def get_num_of_types(self):
        return self.type_section.num_of_entry

    def print_buffer(self):
        # Print 4 bytes per line with index
        for i in range(0, len(self.buffer), 4):
            print(f"{i:04d}: {self.buffer[i:i+4]}")

        return
    