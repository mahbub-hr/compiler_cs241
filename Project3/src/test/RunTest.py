import unittest

# Import all test classes from separate files
from emitter.test_emitter import EmitterTest

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()

    # Add individual test classes to the suite
    suite.addTest(unittest.makeSuite(EmitterTest))

    # Run the test suite
    runner = unittest.TextTestRunner()
    result = runner.run(suite)