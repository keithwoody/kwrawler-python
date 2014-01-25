# Kwrawler

Pronounced "crawler" but I shoe-horned my initials in there, how clever.

Requires nokogiri and ruby-graphviz during runtime.

Crawls a single domain without traversing external links and outputs a sitemap
showing:

1. which static assets each page depends on (imgs, script srcs, and stylesheets)
2. the links between pages

Sitemap can be exported as :png, :jpg, :dot or any GraphViz supported format


