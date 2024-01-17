import unittest
import parser

class TestCalculator(unittest.TestCase):

    def test_get_string(self):
        # global sentence, inp
        parser.sentence = "hello1 world"
        parser.inp = 'h'
        parser.i = 1
        result = parser.get_string()
        self.assertEqual(result, "hello1world", "Should be Hello")

if __name__ == '__main__':
    unittest.main()