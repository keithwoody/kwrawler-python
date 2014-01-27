import kwrawler
import unittest

class KwrawlerTestCase(unittest.TestCase):

    def test_crawl_with_bad_uri(self):
        assert "Invalid URI: 'bad.uri'" == kwrawler.crawl('bad.uri')
    def test_crawl(self):
        assert None == kwrawler.crawl('http://example.com')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(KwrawlerTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
