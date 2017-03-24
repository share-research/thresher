
import requests
import json
import furl

class QueryShare:
##supply query
##maybe move to another class
##TODO add alias list
## TODO parameterize as filters of parameters like: funders, source, title, etc
    def generate_institution_query(self):
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

    def query_share(self, url, query):
        # A helper function that will use the requests library,
        # pass along the correct headers,
        # and make the query we want
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(query)
        return requests.post(url, headers=headers, data=data, verify=False).json()
    
