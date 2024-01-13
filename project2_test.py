import unittest
import arithmatic_expressoin_identifier

class TestCalculator(unittest.TestCase):

    def test_get_string(self):
        # global sentence, inp
        arithmatic_expressoin_identifier.sentence = "hello1 world"
        arithmatic_expressoin_identifier.inp = 'h'
        arithmatic_expressoin_identifier.i = 1
        result = arithmatic_expressoin_identifier.get_string()
        self.assertEqual(result, "hello1world", "Should be Hello")

if __name__ == '__main__':
    unittest.main()