# a class encapsulating the site traversal and sitemap rendering logic for the kwrawler module
import httplib
from urlparse import urlparse, urljoin
import urllib
import time
import re
from bs4 import BeautifulSoup
from pydot import Dot, Node, Edge



class Sitemap(object):
    URI_FAILURE = "failed to read URI '%s'"
    current_contents = None
    base_uri = None
    base_url = None
    current_uri = None
    current_url = None

    def __init__(self):
        self.site_dict = { 'pages': [],
                           'links': {},
                           'assets': { 'imgs': [],
                                       'scripts': [],
                                       'stylesheets': [] }
                         }

    def from_uri(self, uri, render_opts={}):
        """ sets the instance URI and renders a sitemap image
        """
        self.base_uri = uri
        self.base_url = urlparse(uri)
        if self.traverse_site( uri ):
            # img_format = render_opts['format'] or 'png'
            # render_sitemap( img_format, render_options )
            pass
        else:
            return self.URI_FAILURE % uri

    def render_sitemap(self, options={}):
        self.site_graph = Dot(graph_type='digraph')

    def traverse_site(self, uri_str):
        if self.validate_uri( uri_str ):
          # populate site_dict
          print "%d traversing %s" % (int(time.time()), uri_str)
          page_dict = { 'assets': { 'imgs': [],
                                    'scripts': [],
                                    'stylesheets': []
                                  },
                        'links': []
                      }
          self.current_contents = urllib.urlopen( uri_str ).read()
          self.current_uri = uri_str
          self.current_url = urlparse( uri_str )
          self.base_url = self.base_url or self.current_url
          html_doc = BeautifulSoup( self.current_contents )
          # get all scripts, stylesheets and images
          for script in html_doc.find_all('script'):
              src = script.get('src')
              if src is not None:
                  page_dict['assets']['scripts'].append( src )
          sset = set(self.site_dict['assets']['scripts'])
          pset = set(page_dict['assets']['scripts'])
          # list of unique js sources for the site
          self.site_dict['assets']['scripts'] = list( sset | pset )

          for css in html_doc.select('link[rel="stylesheet"]'):
              href = css.get('href')
              if href is not None:
                  page_dict['assets']['stylesheets'].append( href )
          sset = set(self.site_dict['assets']['stylesheets'])
          pset = set(page_dict['assets']['stylesheets'])
          # list of unique stylesheets for the site
          self.site_dict['assets']['stylesheets'] = list( sset | pset )

          for img in html_doc.select('img'):
              src = img.get('src')
              if src is not None and src not in page_dict['assets']['imgs']:
                  page_dict['assets']['imgs'].append( src )
          sset = set(self.site_dict['assets']['imgs'])
          pset = set(page_dict['assets']['imgs'])
          # list of unique images for the site
          self.site_dict['assets']['imgs'] = list( sset | pset )

          # get all internal links on the page
          for link in html_doc.select('a'):
              href = link.get('href').split('#')[0]
              href_uri = urljoin( self.base_url.geturl(), href )
              if self.valid_internal_link(href):
                  if href_uri not in page_dict['links']:
                      page_dict['links'].append( href_uri )
                  if href_uri not in self.site_dict['links'].keys():
                      self.site_dict['links'][ href_uri ] = Link(href_uri, 'new')

          # add the current page and set it as processed
          self.site_dict['pages'].append( Page(self.current_uri, page_dict) )
          self.site_dict['links'][ self.current_uri ] = Link(self.current_uri, 'processed')
          # traverse any linked pages
          for uri, link_obj in self.site_dict['links'].iteritems():
              if link_obj.status is 'new':
                  self.traverse_site( uri )
          return True
        else:
          return False

    def valid_internal_link( self, href ):
        """ returns True if the argument domain is the same as the current url """
        href_url = urlparse( href )
        if href is not None and \
            href_url.netloc in ['', self.base_url.netloc] and \
            re.match(r"""(?!(?:mailto|javascript))""", href):
            return True
        else:
            return False

    def validate_uri(self, uri):
        """ validates a URI is well formed and readable
        """
        if uri is not None:
          u = urlparse( uri )
          conn = httplib.HTTPConnection( u.netloc )
          if u.scheme == 'https':
              conn = httplib.HTTPSConnection( u.netloc )
          path = u.path or "/"
          try:
              conn.request("HEAD", path)
              response = conn.getresponse()
              if response.status == 200:
                  return True
              else:
                  return False
          except Exception, e:
              print self.URI_FAILURE % uri
              return False
          finally:
              conn.close()

class Link(object):
    def __init__(self, uri, status):
      self.uri = uri
      self.status = status

class Page(object):
    def __init__(self, uri, attributes):
      self.uri = uri
      self.attributes = attributes
