from thresher.scraper import Scraper
from thresher.query_share import QueryShare
import furl

#TODO move link parameters to separate configuration file
SHARE_API = 'https://staging-share.osf.io/api/v2/search/creativeworks/_search'
PROD_SHARE_API= 'https://share.osf.io/api/v2/search/creativeworks/_search'

search_url = furl.furl(PROD_SHARE_API)

search_url.args['size'] = 10
#recent_results = requests.get(search_url.url).json()

query_share = QueryShare()
#recent_results = recent_results['hits']['hits']
affiliation_query = query_share.generate_institution_query();
affiliation_results = query_share.query_share(search_url.url, affiliation_query)
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
