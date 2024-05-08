import unittest
from emitter import Emitter
from format import Section, Opcodes, NumberTypes

class TestEmitter(unittest.TestCase):
    def setUp(self):
        self.emitter = Emitter()

    def test_encode_header(self):
        self.assertEqual(self.emitter.encode_header(), Emitter.WASM_BINARY_MAGIC + Emitter.WASM_BINARY_VERSION, "Wasm binary header mismatched")
    
    def test_encode_section(self):
        buffer = bytearray([Section._type.value, 0])
        buffer1 = self.emitter.encode_section(Section._type)

        self.assertEqual(buffer, buffer1)

    def test_add_function_type(self):
        buffer = bytearray([0x60, 0,  1, NumberTypes.i32.value])
        buffer1 = self.emitter.add_function_type([], [NumberTypes.i32.value])

        self.assertEqual(buffer, buffer1)

    def test_write_to_file(self):
        self.emitter.write_to_file("test")

    def test_print_buffer(self):
        self.emitter.print_buffer()


if __name__== '__main__':
    unittest.main()
