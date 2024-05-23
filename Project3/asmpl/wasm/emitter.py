
from wasm.format import SectionID, Opcodes, SectionFormat, Types, ExportKind

class Section:
    def __init__(self, id):
        self.id = id
        self.num_of_entry = 0
        self.buffer = bytearray()

    def add_entry(self, entry_buffer:bytearray):
        self.num_of_entry = self.num_of_entry + 1
        self.buffer.extend(entry_buffer)

        return self.buffer

    def encode(self):
        '''Add two bytes: section_id and section size --> 0'''
        buffer = bytearray([self.num_of_entry])+self.buffer
        size = len(buffer)
        buffer = bytearray([self.id, len(buffer)]) + buffer
        
        return buffer

class Emitter:
    WASM_BINARY_MAGIC = bytearray(b'\x00\x61\x73\x6d')
    WASM_BINARY_VERSION = bytearray(b'\x01\x00\x00\x00')

    def __init__(self):
        self.type_section = Section(SectionID._type.value)
        self.import_section = Section(SectionID._import.value)
        self.function_section = Section(SectionID._func.value)
        self.export_section = Section(SectionID._export.value)
        self.code_section = Section(SectionID._code.value)
        
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

    def init_export_section(self):
        """Always export a default main function"""
        self.add_export("main", ExportKind.func.value, self.type_section.num_of_entry)

        return self.export_section

    def init_import_section(self):
        self.add_import("console", "log", ExportKind.func.value)
        self.add_function_type([Types.i32.value], [])

        return self.import_section

    # def init_code_section(self):
    #     self.code_section = self.encode_section(Section._code.value)
    #     return self.code_section

    def add_result_type(self, rt:list):
        buffer = bytearray()
        buffer.append(len(rt))
        for r in rt:
            buffer.append(r)

        return buffer

    def add_function_type(self, params:list, results:list ):
        buffer = bytearray()
        buffer.append(Types.func.value)
        buffer.extend(self.add_result_type(params))
        buffer.extend(self.add_result_type(results))

        self.type_section.add_entry(buffer)

        return buffer
    
    def add_import(self, module_name, field_name, imp_kind, imp_signature_idx=0):
        buffer = bytearray([len(module_name)]) +  module_name.encode("utf-8")+ bytearray([len(field_name)]) + field_name.encode("utf-8")+ bytearray([imp_kind, imp_signature_idx])
        self.import_section.add_entry(buffer)

        return buffer

    def add_func(self):
        buffer = bytearray([self.type_section.num_of_entry-1])
        self.function_section.add_entry(buffer)

        return buffer

    def add_export(self, exp_name, exp_kind, func_idx=0):
        buffer = bytearray([len(exp_name)])+  exp_name.encode("utf-8") + bytearray([exp_kind, func_idx])
        self.export_section.add_entry(buffer)
        return buffer
        
    def add_func_body(self, num_of_local, body:bytearray):
        buffer = bytearray([num_of_local]) + body
        buffer = bytearray([len(buffer)]) + buffer
        self.code_section.add_entry(buffer)

        return buffer

    def encode_module(self):
        buffer = self.encode_header() + self.type_section.encode() + self.import_section.encode()+ self.function_section.encode() + self.export_section.encode() + self.code_section.encode()
        return buffer

    def write_to_file(self, filename, buffer):
        with open(filename+".wasm", "wb") as f:
            f.write(buffer)
        
        return

    def print_buffer(self):
        # Print 4 bytes per line with index
        for i in range(0, len(self.buffer), 4):
            print(f"{i:04d}: {self.buffer[i:i+4]}")

        return
    