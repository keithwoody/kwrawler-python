# a class encapsulating the site traversal and sitemap rendering logic for the kwrawler module
import httplib
from urlparse import urlparse
import urllib
import time
from bs4 import BeautifulSoup

class Sitemap(object):
    URI_FAILURE = "failed to read URI '%s'"
    current_contents = None

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
        self.uri = uri
        if self.traverse_site( uri ):
            # img_format = render_opts['format'] or 'png'
            # render_sitemap( img_format, render_options )
            pass
        else:
            return self.URI_FAILURE % uri

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
          soup = BeautifulSoup( self.current_contents )
          # get all scripts, stylesheets and images
          for script in soup.find_all('script'):
              src = script.get('src')
              if src is not None:
                  page_dict['assets']['scripts'].append( src )
          sset = set(self.site_dict['assets']['scripts'])
          pset = set(page_dict['assets']['scripts'])
          # list of unique js sources for the site
          self.site_dict['assets']['scripts'] = list( sset | pset )

          for css in soup.select('link[rel="stylesheet"]'):
              href = css.get('href')
              if href is not None:
                  page_dict['assets']['stylesheets'].append( href )
          sset = set(self.site_dict['assets']['stylesheets'])
          pset = set(page_dict['assets']['stylesheets'])
          # list of unique stylesheets for the site
          self.site_dict['assets']['stylesheets'] = list( sset | pset )

          for img in soup.select('img'):
              src = img.get('src')
              if src is not None and src not in page_dict['assets']['imgs']:
                  page_dict['assets']['imgs'].append( src )
          sset = set(self.site_dict['assets']['imgs'])
          pset = set(page_dict['assets']['imgs'])
          # list of unique images for the site
          self.site_dict['assets']['imgs'] = list( sset | pset )

          # get all internal links on the page
          # add the current page and set it as processed
          # traverse any linked pages
          return True
        else:
          return False

    def validate_uri(self, uri):
        """ validates a URI is well formed and readable
        """
        if uri is not None:
          u = urlparse( uri )
          conn = httplib.HTTPConnection( u.netloc )
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

