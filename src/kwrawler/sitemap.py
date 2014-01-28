# a class encapsulating the site traversal and sitemap rendering logic for the kwrawler module
import httplib
from urlparse import urlparse

class Sitemap(object):
    URI_FAILURE = "failed to read URI '%s'"

    def __init__(self):
        self.uri = "URI must be set"

    def from_uri(self, uri):
        """ sets the instance URI and renders a sitemap image
        """
        self.uri = uri
        if self.validate_uri():
            # traverse_site( uri )
            pass
        else:
            return self.URI_FAILURE % uri

    def validate_uri(self):
        """ validates a URI is well formed and readable
        """
        if self.uri is not None:
          u = urlparse( self.uri )
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
              print self.URI_FAILURE % self.uri
              return False
          finally:
              conn.close()

