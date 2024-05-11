import unittest
from emitter import Emitter, Section
from format import SectionID, Opcodes, Types, ExportKind

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
        buffer = bytearray([SectionID._import.value, 0xf, 1, 7]) + b"console"+ bytearray([3]) + b"log" + bytearray([ExportKind.func.value, 0])
        self.emitter.init_imprt_section()
        self.assertEqual(buffer, self.emitter.import_section.encode())

    def test_


if __name__== '__main__':
    unittest.main()
