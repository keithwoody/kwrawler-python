# A python translation of a demo ruby gem
from urlparse import urlparse
# import 'sitemap'


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
        filename = 'sitemap.png'
        with open(filename, 'w') as sitemap_img:
            sitemap_img.write("TODO")
    # sitemap = Sitemap()
    # sitemap.from_uri( uri )
