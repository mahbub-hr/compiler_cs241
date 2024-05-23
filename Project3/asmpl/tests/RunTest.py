import unittest

# Import all test classes from separate files
from test_emitter import TestEmitter
if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()

    # Add individual test classes to the suite
    suite.addTest(unittest.makeSuite(TestEmitter))

    # Run the test suite
    runner = unittest.TextTestRunner()
    result = runner.run(suite)