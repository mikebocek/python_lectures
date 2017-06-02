import unittest

def run_tests(test_case):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
    unittest.TextTestRunner(verbosity = 2).run(suite)
