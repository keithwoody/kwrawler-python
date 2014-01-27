import kwrawler
import test_kwrawler

def suite():
    import unittest
    import doctest
    suite = unittest.TestSuite()
    suite.addTests(doctest.DocTestSuite(kwrawler))
    suite.addTests(test_kwrawler.suite())
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
