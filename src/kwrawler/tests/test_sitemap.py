from kwrawler import sitemap
import unittest
import os.path
from mock import patch, Mock
from io import StringIO
import pydot

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

    def test_render_sitemap_should_build_the_site_graph_just_once(self):
        assert self.sitemap_obj.site_graph is None
        self.sitemap_obj.render_sitemap()
        g1 = self.sitemap_obj.site_graph
        assert g1 is not None
        self.sitemap_obj.render_sitemap()
        g2 = self.sitemap_obj.site_graph
        self.assertEqual(g1, g2)

    def test_render_sitemap_should_default_to_png_output(self):
        if os.path.isfile('sitemap.png'):
            os.remove('sitemap.png')
        assert False == os.path.isfile('sitemap.png')
        with patch('urllib.urlopen') as mock_get:
            mock_get.return_value = self.mock_response
            self.sitemap_obj.traverse_site( 'http://example.com/' )
            self.sitemap_obj.render_sitemap()
        assert True == os.path.isfile('sitemap.png')

    def test_render_sitemap_should_use_format_from_options_hash(self):
        if os.path.isfile('sitemap.jpg'):
            os.remove('sitemap.jpg')
        self.assertEqual( False, os.path.isfile('sitemap.jpg') )
        with patch('urllib.urlopen') as mock_get:
            mock_get.return_value = self.mock_response
            self.sitemap_obj.traverse_site( 'http://example.com/' )
            self.sitemap_obj.render_sitemap({'format': 'jpg'})
        self.assertEqual( True, os.path.isfile('sitemap.jpg') )

    def test_render_sitemap_should_use_filename_from_options_hash(self):
        if os.path.isfile('sitemap.JPG'):
            os.remove('sitemap.JPG')
        self.assertEqual( False, os.path.isfile('sitemap.JPG') )
        with patch('urllib.urlopen') as mock_get:
            mock_get.return_value = self.mock_response
            self.sitemap_obj.traverse_site( 'http://example.com/' )
            self.sitemap_obj.render_sitemap({'format': 'jpg', 'filename': 'sitemap.JPG'})
        self.assertEqual( True, os.path.isfile('sitemap.JPG') )

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

    def test_build_site_graph_should_init_site_graph(self):
        self.sitemap_obj.build_site_graph()
        assert self.sitemap_obj.site_graph is not None
        assert isinstance( self.sitemap_obj.site_graph, pydot.Graph )

    def test_build_site_graph_should_add_a_label_for_the_image(self):
        self.sitemap_obj.build_site_graph()
        assert self.sitemap_obj.site_graph.get_label() == 'Sitemap for "None"'

    def test_build_site_graph_should_coalesce_duplicated_edges(self):
        self.sitemap_obj.build_site_graph()
        self.assertEqual( True, self.sitemap_obj.site_graph.get_simplify() )

    def test_build_site_graph_should_add_a_node_for_each_page(self):
        with patch.object(self.sitemap_obj, 'validate_uri') as mocked_validate_uri:
            mocked_validate_uri.return_value = True
            with patch('urllib.urlopen') as mock_get:
                mock_get.return_value = self.mock_response
                self.sitemap_obj.traverse_site( 'http://example.com/' )
                self.sitemap_obj.build_site_graph()
                node_cnt = len( self.sitemap_obj.site_graph.get_nodes() )
                assert 2 == node_cnt

    def test_build_site_graph_should_add_an_edge_for_each_link_between_pages(self):
        with patch.object(self.sitemap_obj, 'validate_uri') as mocked_validate_uri:
            mocked_validate_uri.return_value = True
            with patch('urllib.urlopen') as mock_get:
                mock_get.return_value = self.mock_response
                self.sitemap_obj.traverse_site( 'http://example.com/' )
                self.sitemap_obj.build_site_graph()
                edge_cnt = len( self.sitemap_obj.site_graph.get_edges() )
                assert 1 == edge_cnt

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(SitemapTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
