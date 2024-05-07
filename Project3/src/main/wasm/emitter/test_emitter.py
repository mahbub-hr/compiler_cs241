import unittest
from emitter import Emitter

class TestEmitter(unittest.TestCase):
    def setUp(self):
        self.emitter = Emitter()

    def test_header(self):
        self.assertEqual(self.emitter.header(), Emitter.WASM_BINARY_MAGIC + Emitter.WASM_BINARY_VERSION, "Wasm binary header mismatched")
    
    def test_print_buffer(self):
        self.emitter.print_buffer()


if __name__== '__main__':
    unittest.main()
