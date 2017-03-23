## goals for next week
## get something working with DOIs
## have list of url's coming SHARE query
## pull just content from first level
## store as files
## store metadata record
## fish for interest and next steps


import requests
import furl

from urllib.parse import urlparse

#def get_links(source_page):
    #A method to return a list of links found embedded in page

#def get_download_links()
#create function get mime_type; returns nil if unknown
def get_mime_type(url):
    formatted_url = furl.furl(url)
    try:
        mime_response = requests.get(formatted_url.url)
        mime_type = mime_response.headers.get('content-type')
        return mime_type
    except:
        print ("Exception found for url: ", url)
        None

def get_root_url(url):
    parsed_uri = urlparse(url)
    root = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return root

#import the library used to query a website
from bs4 import BeautifulSoup

#put into method once working
#url = "https://www.nsf.gov/awardsearch/showAward?AWD_ID=1560089"
#url = "https://curate.nd.edu/show/ht24wh26g7d"
#csv file from page above
#url = "https://curate.nd.edu/downloads/hx11xd09r8t"

#start with DOI links from SHARE
# one class get links
#next class get objects
#one class save files
#one class create csv

#excavation example from researchgate
url = "http://dx.doi.org/10.13140/RG.2.1.4495.1923"

page_url = furl.furl(url)
#search_url.args['size'] = 3
response = requests.get(page_url.url)

#first check to see if content type is non html
mime_type = response.headers.get('content-type')
print("Root url: ", response.url)
#get url domain after redirect
root_url = get_root_url(response.url)
print("Root domain: ", root_url)
print("Root link mime_type: ", mime_type)

soup = BeautifulSoup(response.text, "html.parser")

#TODO: check mime type and detect if a file versus html content
#print(response.headers.get('content-type'))
#print(response.text)

#TODO ignore CSS files (add an ignore extension list)
#TODO add an ignore MIME/TYPE list (configurable parameter file)
print("         ")
print("----------Printing Soup--------------")
for a in soup.find_all('a', href=True):
    href = a['href']
    if not href.startswith("http"):
        full_url = root_url + href
    else:
        full_url = href

    content_url = furl.furl(full_url)
    mime_type = get_mime_type(full_url)
    if mime_type is not None:
        if "text/html" not in mime_type:
            print("Found content link:", content_url, " MIME-TYPE: ", mime_type)
    else:
        print("Found invalid URL:", content_url)



# get list of records from SHARE as JSON-LD
# from record extract links
# log metadata record
# get html from links (if html find downloads directly embedded)
# if none found log html as content
# log source content(s) found and associated link used 
# log rights statement for review (if available)
# store content, create folder, store files
# spit out into csv file?

#TODO later more sophisticated follows of html
#TODO later filter by data provider to SHARE (DataCite, ResearchGate, etc)
#TODO incorporate feeding to more formal webcrawler tools (guidance from group, participation)

#saving content: create folder for each item

#Start look for application/pdf
#Others look for other content

#TODO incorporate full characterization and virus checking

#Challenges
#Downloads hidden behind javascript or button
