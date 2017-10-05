from TestHarnessTestCase import TestHarnessTestCase

class TestHarnessTester(TestHarnessTestCase):
    def testSyntax(self):
        """
        Test for SYNTAX PASS status in the TestHarness
        """

        # Test that the SYNTAX PASS status message properly displays
        output = self.runTests('-i', 'syntax')
        self.assertIn('SYNTAX PASS', output)

        # Test that the SYNTAX PASS status message properly displays
        output = self.runTests('--check-input', '-i', 'syntax')
        self.assertIn('SYNTAX PASS', output)

        # Check that SYNTAX PASS test was not run
        output = self.runTests('--check-input', '-i', 'no_syntax')
        self.assertNotIn('SYNTAX PASS', output)

        # check that parser errors print correctly
        output = self.runExceptionTests('--check-input', '-i', 'parse_errors')
        self.assertIn('Parser Errors', output)
