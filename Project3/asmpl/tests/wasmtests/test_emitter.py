import unittest

from emitter import Emitter, Section
from format import SectionID, Opcodes, Types, ExportKind

def compare_bytearray(arr1, arr2):
    l = min(len(arr1), len(arr2))

    for i in range(0, l):
        if arr1[i] != arr2[i]:
            print(f"Byte mismatch found at position {i}: {arr1[i]} != {arr2[i]}")
            return
         
class TestEmitter(unittest.TestCase):
    def setUp(self):
        self.emitter = Emitter()
        self.section = Section(SectionID._type.value)
   
    def test_encode_header(self):
        self.assertEqual(self.emitter.encode_header(), Emitter.WASM_BINARY_MAGIC + Emitter.WASM_BINARY_VERSION, "Wasm binary header mismatched")
    
    def test_encode_section(self):
        buffer = bytearray([SectionID._type.value, 1, 0])
        buffer1 = self.section.encode()

        self.assertEqual(buffer, buffer1)

    def test_add_function_type(self):
        buffer = bytearray([Types.func.value, 2, Types.i32.value, Types.i64.value,  1, Types.i32.value])
        buffer1 = self.emitter.add_function_type([Types.i32.value, Types.i64.value], [Types.i32.value])

        self.assertEqual(buffer, buffer1)

    def test_init_import_section(self):
        # 0000008: 01                                        ; section code
        # 0000009: 05                                        ; section size (guess)
        # 000000a: 01                                        ; num types
        # ; func type 0
        # 000000b: 60                                        ; func
        # 000000c: 01                                        ; num params
        # 000000d: 7f                                        ; i32
        # 000000e: 00                                        ; num results
        buffer = bytearray([SectionID._import.value, 0xf, 1, 7]) + b"console"+ bytearray([3]) + b"log" + bytearray([ExportKind.func.value, 0])
        buffer1 = bytearray([SectionID._type.value, 5, 1, Types.func.value, 1, 0x7f, 0])
        self.emitter.init_import_section()
        self.assertEqual(buffer, self.emitter.import_section.encode())
        self.assertEqual(buffer1, self.emitter.type_section.encode())

# ; section "Export" (7)
# 0000027: 07                                        ; section code
# 0000028: 08                                       ; section size (guess)
# 0000029: 01                                        ; num exports
# 000002a: 04                                        ; string length
# 000002b: 6d 61 69 6e                                  main  ; export name
# 000002e: 00                                        ; export kind
# 000002f: 00                                        ; export func index
    def test_init_export_section(self):
        buffer = bytearray([SectionID._export.value, 0x8, 1, 4]) + b"main"+ bytearray([ExportKind.func.value, 0])
        self.emitter.init_export_section()
        self.assertEqual(buffer, self.emitter.export_section.encode())

# 0000000: 0061 736d                                 ; WASM_BINARY_MAGIC
# 0000004: 0100 0000                                 ; WASM_BINARY_VERSION
# ; section "Type" (1)
# 0000008: 01                                        ; section code
# 0000009: 00                                        ; section size (guess)
# 000000a: 02                                        ; num types
# ; func type 0
# 000000b: 60                                        ; func
# 000000c: 01                                        ; num params
# 000000d: 7f                                        ; i32
# 000000e: 00                                        ; num results
# ; func type 1
# 000000f: 60                                        ; func
# 0000010: 00                                        ; num params
# 0000011: 00                                        ; num results
# 0000009: 08                                        ; FIXUP section size
# ; section "Import" (2)
# 0000012: 02                                        ; section code
# 0000013: 00                                        ; section size (guess)
# 0000014: 01                                        ; num imports
# ; import header 0
# 0000015: 07                                        ; string length
# 0000016: 636f 6e73 6f6c 65                        console  ; import module name
# 000001d: 03                                        ; string length
# 000001e: 6c6f 67                                  log  ; import field name
# 0000021: 00                                        ; import kind
# 0000022: 00                                        ; import signature index
# 0000013: 0f                                        ; FIXUP section size
# ; section "Function" (3)
# 0000023: 03                                        ; section code
# 0000024: 00                                        ; section size (guess)
# 0000025: 01                                        ; num functions
# 0000026: 01                                        ; function 0 signature index
# 0000024: 02                                        ; FIXUP section size
# ; section "Export" (7)
# 0000027: 07                                        ; section code
# 0000028: 00                                        ; section size (guess)
# 0000029: 01                                        ; num exports
# 000002a: 03                                        ; string length
# 000002b: 6164 64                                  add  ; export name
# 000002e: 00                                        ; export kind
# 000002f: 01                                        ; export func index
# 0000028: 07                                        ; FIXUP section size
# ; section "Code" (10)
# 0000030: 0a                                        ; section code
# 0000031: 00                                        ; section size (guess)
# 0000032: 01                                        ; num functions
# ; function body 0
# 0000033: 00                                        ; func body size (guess)
# 0000034: 00                                        ; local decl count
# 0000035: 41                                        ; i32.const
# 0000036: 2b                                        ; i32 literal
# 0000037: 41                                        ; i32.const
# 0000038: 36                                        ; i32 literal
# 0000039: 6a                                        ; i32.add
# 000003a: 10                                        ; call
# 000003b: 00                                        ; function index
# 000003c: 0b                                        ; end
# 0000033: 09                                        ; FIXUP func body size
# 0000031: 0b 

    def test_add_function(self):
        self.test_add_function_type()
        buffer = bytearray([3, 2, 1, 0])
        self.emitter.add_func()
        self.assertEqual(buffer, self.emitter.function_section.encode())
    
    def test_add_function_after_default_import(self):
        buffer = bytearray([3,2,1,1])
        self.emitter.init_import_section()
        self.emitter.add_function_type([], [])
        self.emitter.add_func()
        self.assertEqual(buffer, self.emitter.function_section.encode())


    def test_add_func_body(self):
        body = bytearray([0x41, 0x2b, 0x41, 0x36, 0x6a, 0x10, 0, 0x0b])
        self.emitter.add_func_body(0, body)
        buffer1 = self.emitter.code_section.encode()
        buffer =  bytearray([0x0a, 0x0b, 1, 9, 0]) + body

        self.assertEqual(buffer, buffer1)

    def test_simple_print(self):
        import os
        path = os.path.realpath(__file__)
        dir_name = os.path.dirname(path)
        path = os.path.join(dir_name, "hello.wasm")
        with open(path, 'rb') as wasm_file:
            wasm_bytes = bytearray(wasm_file.read())

        self.emitter.init_import_section()
        self.emitter.init_export_section()
        self.add_local_func([], [], 0, bytearray([0x41, 0x2b, 0x41, 0x36, 0x6a, 0x10, 0, 0x0b]))
        buffer = self.emitter.encode_module()

        with open(os.path.join(dir_name, "../WebassemblyTest/new_hello.wasm"), 'wb') as f:
            f.write(buffer)

        compare_bytearray(wasm_bytes, buffer)
        self.assertEqual(len(wasm_bytes), len(buffer))
        self.assertEqual(wasm_bytes, buffer)

    def add_local_func(self, params: list, results: list, local_decl_count, body):
        self.emitter.add_function_type(params, results)
        self.emitter.add_func()
        self.emitter.add_func_body(local_decl_count, body)


if __name__== '__main__':

    unittest.main()
