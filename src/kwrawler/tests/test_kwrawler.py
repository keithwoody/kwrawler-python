import kwrawler
import unittest
import os.path

class KwrawlerTestCase(unittest.TestCase):

    def test_crawl_should_take_a_string_argument(self):
      self.assertRaises(TypeError, kwrawler.crawl)

    def test_crawl_should_exit_gracefully_if_uri_is_invalid(self):
        assert "Invalid URI: 'bad.uri'" == kwrawler.crawl('bad.uri')

    def test_crawl_should_export_sitemap_as_an_image(self):
        if os.path.isfile('sitemap.png'):
            os.remove('sitemap.png')
        assert False == os.path.isfile('sitemap.png')
        kwrawler.crawl('http://example.com')
        assert True == os.path.isfile('sitemap.png')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(KwrawlerTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
