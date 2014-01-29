# A python translation of a demo ruby gem
from urlparse import urlparse
from sitemap import Sitemap


def crawl( uri ):
    """
    >>> crawl( 'http://example.com' )
    create and render sitemap
    """
    u = urlparse( uri )
    if u.scheme == '' and u.netloc == '':
        return "Invalid URI: '%s'" % (uri)
    else:
        print "create and render sitemap"
        sitemap = Sitemap().from_uri( uri )
