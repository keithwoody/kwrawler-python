from kwrawler import sitemap
import unittest
import os.path
from mock import patch, Mock
from io import StringIO

class SitemapTestCase(unittest.TestCase):
    def setUp(self):
        self.sitemap_obj = sitemap.Sitemap()
        self.mock_html = """
        <html>
          <head>
            <script src="local.js"></script>
            <link rel="stylesheet" href="local.css"/>
          </head>
          <body>
            <a href="/internal">internal</a>
            <a href="/internal#with_anchor">internal</a>
            <a href="http://external.com/about">external</a>
            <img src="local.png"/>
            <hr/>
            <img src="local.png"/>
          </body>
        </html>
        """
        self.mock_response = StringIO( unicode(self.mock_html) )

    def test_from_uri_should_require_a_URI(self):
        with self.assertRaises( TypeError ):
            self.sitemap_obj.from_uri()
        self.sitemap_obj.from_uri( 'http://example.com' )
        self.assertEqual( 'http://example.com', self.sitemap_obj.base_uri )

    def test_from_uri_should_exit_gracefully_for_a_bad_uri(self):
        error_msg = "failed to read URI 'http://not.valid'"
        self.assertEqual( error_msg, self.sitemap_obj.from_uri('http://not.valid') )

    def test_validate_uri(self):
        self.assertEqual(True, self.sitemap_obj.validate_uri("http://example.com/"))
        self.assertEqual(False, self.sitemap_obj.validate_uri("http://not.valid/"))

    def test_render_sitemap_1(self):
        # assert False
        pass

    def test_retrieve(self):
        # assert False
        pass

    def test_traverse_site_should_set_current_contents(self):
        assert None == self.sitemap_obj.current_contents
        self.sitemap_obj.traverse_site( 'http://example.com/' )
        assert None != self.sitemap_obj.current_contents

    def test_traverse_site_should_add_unique_js_sources_to_assets(self):
        with patch('urllib.urlopen') as mock_get:
            mock_get.return_value = self.mock_response
            self.sitemap_obj.traverse_site( 'http://example.com/' )
            js_lst = self.sitemap_obj.site_dict['assets']['scripts']
            self.assertEqual( True, 'local.js' in js_lst )
            self.assertEqual( 1, len(js_lst) )

    def test_traverse_site_should_add_unique_stylesheets_sources_to_assets(self):
        with patch('urllib.urlopen') as mock_get:
            mock_get.return_value = self.mock_response
            self.sitemap_obj.traverse_site( 'http://example.com/' )
            css_lst = self.sitemap_obj.site_dict['assets']['stylesheets']
            self.assertEqual( True, 'local.css' in css_lst )
            self.assertEqual( 1, len(css_lst) )

    def test_traverse_site_should_add_unique_images_sources_to_assets(self):
        with patch('urllib.urlopen') as mock_get:
            mock_get.return_value = self.mock_response
            self.sitemap_obj.traverse_site( 'http://example.com/' )
            img_lst = self.sitemap_obj.site_dict['assets']['imgs']
            self.assertEqual( True, 'local.png' in img_lst )
            self.assertEqual( 1, len(img_lst) )

    def test_traverse_site_should_add_internal_links_to_site_dict(self):
        with patch('urllib.urlopen') as mock_get:
            mock_get.return_value = self.mock_response
            self.sitemap_obj.traverse_site( 'http://example.com/' )
            link_lst = self.sitemap_obj.site_dict['links'].keys()
            assert 'http://example.com/internal' in link_lst
            assert 'http://example.com/internal#with_anchor' not in link_lst
            assert 'http://external.com/about' not in link_lst
            print link_lst
            self.assertEqual( 2, len(link_lst) )

    def test_traverse_site_should_add_a_page_for_unique_uris(self):
        # fake validating URIs so it doesn't fail on example.com/internal
        with patch.object(self.sitemap_obj, 'validate_uri') as mocked_validate_uri:
            mocked_validate_uri.return_value = True
            with patch('urllib.urlopen') as mock_get:
                mock_get.return_value = self.mock_response
                self.sitemap_obj.traverse_site( 'http://example.com/' )
                page_lst = [ p.uri for p in self.sitemap_obj.site_dict['pages'] ]
                assert 'http://example.com/' in page_lst
                assert 'http://example.com/internal' in page_lst
                self.assertEqual(2, len( page_lst ))

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
