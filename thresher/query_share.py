SHARE_API = 'https://staging-share.osf.io/api/v2/search/creativeworks/_search'
PROD_SHARE_API= 'https://share.osf.io/api/v2/search/creativeworks/_search'

import requests
import json
import furl

search_url = furl.furl(PROD_SHARE_API)
search_url.args['size'] = 3
recent_results = requests.get(search_url.url).json()

recent_results = recent_results['hits']['hits']

print('The request URL is {}'.format(search_url.url))
print('----------')
for result in recent_results:
    print(
        '{} -- from {}'.format(
            result['_source']['title'],
            result['_source']['identifiers']
        )
    )
    print(result)
