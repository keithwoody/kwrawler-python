from kwrawler import sitemap
import unittest
import os.path

class SitemapTestCase(unittest.TestCase):
    def setUp(self):
        self.sitemap_obj = sitemap.Sitemap()

    def test_from_uri_should_require_a_URI(self):
        with self.assertRaises( TypeError ):
            self.sitemap_obj.from_uri()
        self.sitemap_obj.from_uri( 'http://example.com' )
        self.assertEqual( 'http://example.com', self.sitemap_obj.uri )

    def test_from_uri_should_exit_gracefully_for_a_bad_uri(self):
        error_msg = "failed to read URI 'http://not.valid'"
        self.assertEqual( error_msg, self.sitemap_obj.from_uri('http://not.valid') )

    def test_validate_uri(self):
        self.sitemap_obj.uri = "http://example.com/"
        self.assertEqual(True, self.sitemap_obj.validate_uri())
        self.sitemap_obj.uri = "http://not.valid/"
        self.assertEqual(False, self.sitemap_obj.validate_uri())

    def test_render_sitemap_1(self):
        # assert False
        pass

    def test_retrieve(self):
        # assert False
        pass

    def test_traverse_site(self):
        # assert False
        pass

    def test_build_site_graph(self):
        # assert False
        pass


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(SitemapTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
