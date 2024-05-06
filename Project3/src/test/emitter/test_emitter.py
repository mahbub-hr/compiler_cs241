import unittest
from main.emitter import Emitter

class TestEmitter(unittest.TestCase):
    def setUp(self):
        self.emitter = Emitter()

    def test_print_buffer(self):
        self.emitter.print_buffer()


if __name__== '__main__':
    unittest.main()
