# thresher

A utility to harvest research content from research activity aggregated by SHARE from over 150 data sources.  With a given query to SHARE it supplies a list content links that are then crawled download links to content.  This content is then downloaded and linked to the corresponding JSON-LD record from SHARE.

Install Dependendencies

-Python 3.5

- Python wget library
pip install wget

-Slugify
pip install python-slugify

Install Beautiful Soup according to instructions here:

https://www.crummy.com/software/BeautifulSoup/bs4/doc/