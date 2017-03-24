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

#import the library used to parse an html page
from bs4 import BeautifulSoup

class Scraper:
    #def __init__(self):
        

    #create function get mime_type; returns nil if unknown
    def get_mime_type(self, url):
        formatted_url = furl.furl(url)
        try:
            #use stream=True so it does not try to pre-download the content
            mime_response = requests.get(formatted_url.url, stream=True)
            mime_type = mime_response.headers.get('content-type')
            return mime_type
        except:
            print ("Exception found for url: ", url)
            None
            
    def get_root_url(self, url):
        parsed_uri = urlparse(url)
        root = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return root
    


    #Returns a list of content url's and their mime/types from a given html page
    #That are not of mime-type 'text/html'
    def get_content_urls_from_html_page(self, url):
        print("starting get content links")
        page_url = furl.furl(url)
        response = requests.get(page_url.url, stream=True)

        print("getting mime-type for first link")
        #first check to see if content type is html
        mime_type = response.headers.get('content-type')

        #create dictionary (hash) for links and content
        content_links = {}
        
        if "text/html" in mime_type:
            #get url domain after redirect
            root_url = self.get_root_url(response.url)

            soup = BeautifulSoup(response.text, "html.parser")

            #TODO ignore CSS files (add an ignore extension list)
            #TODO add an ignore MIME/TYPE list (configurable parameter file)

            print("starting for loop")
            for a in soup.find_all('a', href=True):
                print("iteration")
                href = a['href']

                if not href.startswith("http"):
                    full_url = root_url + href
                else:
                    full_url = href

                #only if not already found on page
                content_url = furl.furl(full_url)

                if content_url.url not in content_links:
                    mime_type = self.get_mime_type(full_url)
                    if mime_type is not None:
                        if "text/html" not in mime_type:
                            print("Found content link:", content_url, " MIME-TYPE: ", mime_type)
                            content_links[content_url.url] = mime_type
                    else:
                        print("Found invalid URL:", content_url)
        else:
            #just return first page if not html
            content_links[page_url.url] = mime_type
            
        if not content_links:
            #if no links found just return first page
            content_links[page_url.url] = mime_type

        return content_links

#end def class Scraper

#excavation example from researchgate
#url = "http://dx.doi.org/10.13140/RG.2.1.4495.1923"
#get hash of url's and mime_types for non html content
#content_links = get_content_urls_from_html_page(url)
#print(content_links)
#url2 = "https://curate.nd.edu/show/ht24wh26g7d"
#content_links2 = get_content_urls_from_html_page(url2)
#print(content_links2)
#url = "https://www.nsf.gov/awardsearch/showAward?AWD_ID=1560089"
#url = "https://curate.nd.edu/show/ht24wh26g7d"
#csv file from page above
#url = "https://curate.nd.edu/downloads/hx11xd09r8t"

#do share query
#get links
#start with DOI links from SHARE
# one class get links
#next class get objects
#one class save files
#one class create csv

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
#TODO create unit tests

#TODO develop Ruby support as well

#Challenges
#Downloads hidden behind javascript or button
