#TODO move link parameters to separate configuration file
SHARE_API = 'https://staging-share.osf.io/api/v2/search/creativeworks/_search'
PROD_SHARE_API= 'https://share.osf.io/api/v2/search/creativeworks/_search'

import requests
import json
import furl

from scraper import Scraper

##supply query
##maybe move to another class
##TODO add alias list
## TODO parameterize as filters of parameters like: funders, source, title, etc
def generate_institution_query():
    affiliation_query = {
        "size": 10000,
        "query": {
            "bool": {
                "must": {
                    "query_string": {
                        "query": "University of Notre Dame"
                        }
                    },
                "filter": [
                    {
                        "term": {
                            "sources": "DataCite MDS"
                            }
                        }
                        #"term": {
                        #    "contributors": "University Of Notre Dame"
                    #}
#                        },
                    ]
                }
            }
        }
    return affiliation_query

def query_share(url, query):
    # A helper function that will use the requests library,
    # pass along the correct headers,
    # and make the query we want
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(query)
    return requests.post(url, headers=headers, data=data, verify=False).json()

search_url = furl.furl(PROD_SHARE_API)
search_url.args['size'] = 10
#recent_results = requests.get(search_url.url).json()

#recent_results = recent_results['hits']['hits']
affiliation_query = generate_institution_query();
affiliation_results = query_share(search_url.url, affiliation_query)
records = affiliation_results['hits']['hits']

#for row in records:
#    if i == 0:
#        fieldnames = row['_source'].keys()
#        print(fieldnames);
        #            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
#            writer.writeheader()
#        i = i + 1
#        writer.writerow(row['_source'])    

print('The request URL is {}'.format(search_url.url))
print('----------')
scrap = Scraper()
i = 0
for result in records:
    i += 1
    print("---------------------------------")
    print(
        'Getting Content for Record {}: {} -- from {}'.format(
            i,
            result['_source']['title'],
            result['_source']['identifiers']
        )
    )
    for identifier in result['_source']['identifiers']:
        if "http" in identifier:
            print ("Getting links for identifer: ", identifier)
            links = scrap.get_content_urls_from_html_page(identifier)
            print("Links Found are: ", links)


# call query_share
# get list of records
# grab identifiers from records
# get content links for each record
# download content for each record
