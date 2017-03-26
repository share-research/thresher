from thresher.scraper import Scraper
from thresher.query_share import QueryShare
import furl
import csv
import os
from slugify import slugify
import wget
import json

### Possibly convert this to docopt script in the future
###

class Thresher:
    #assumes that links is a list of dictionaries with the keys as a content-link and mimetype
    def create_manifest(self,directory,filename,content_items):
        print('---begin writing manifest file---')

        #if directory exists just catch error
        try:
            os.mkdir(directory)
        except:
            pass

        #get current directory
        working_directory = os.getcwd()
        try :
            os.chdir(directory)
            with open(filename, 'w') as csvfile:
                i = 0
                for content in content_items:
                    if i == 0:
                        fieldnames = content.keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                        writer.writeheader()
                    writer.writerow(content)
                    i = i + 1
        except:
            pass
        #change back to working directory
        os.chdir(working_directory)
        print('---done writing manifest file---')

    def write_json_file(self,directory,filename,json_obj):
        print('---begin writing json metadata file---')

        #if directory exists just catch error
        try:
            os.mkdir(directory)
        except:
            pass

        #get current directory
        working_directory = os.getcwd()
        try :
            os.chdir(directory)
            with open(filename, 'w') as outfile:
                #print("writing json ", json_obj)
                #json_str = json.dumps(json_obj)
                #outfile.write(json_str)
                #print ("json str is", json_str)
                json.dump(json_obj, outfile, ensure_ascii=False)
            outfile.close()
        except Exception as inst:
            print("had exception on write to json: ", inst)
            pass
        #change back to working directory
        os.chdir(working_directory)
        print('---done writing json metadata file---')

    def prepare_link_data(self,links):
        #converts link hash to list of dictionaries with content-type and mime-type as keys
        link_list = []
        for link in links:
            link_dict = {}
            link_dict['content-link'] = link
            link_dict['mime-type'] = links[link]
            link_list.append(link_dict)
        return link_list

    def create_data_folder(self,dir_name):
        #if exists just catch error
        try:
            os.mkdir(dir_name)
        except:
            pass

    def download_content_file(self,dir_name,url):
        working_directory = os.getcwd()
        filename = None
        
        #if directory exists just catch error
        try:
            os.mkdir(dir_name)
        except:
            pass

        try:
            os.chdir(dir_name)
            filename = wget.download(url)
        except Exception as inst:
            print("had exception on wget: ", inst)
            pass
        
        #reset directory
        os.chdir(working_directory)
        return filename

    def thresher(self):
        return

## End Thresher class

#TODO move link parameters to separate configuration file
SHARE_API = 'https://staging-share.osf.io/api/v2/search/creativeworks/_search'
PROD_SHARE_API= 'https://share.osf.io/api/v2/search/creativeworks/_search'

search_url = furl.furl(PROD_SHARE_API)

search_url.args['size'] = 20
#recent_results = requests.get(search_url.url).json()

query_share = QueryShare()
#recent_results = recent_results['hits']['hits']
affiliation_query = query_share.generate_institution_query();
affiliation_results = query_share.query_share(search_url.url, affiliation_query)
records = affiliation_results['hits']['hits']

print('The request URL is {}'.format(search_url.url))
print('----------')
scrape = Scraper()
thresh = Thresher()
i = 0

#create data folder
print("--------------creating data folder-----------")
thresh.create_data_folder("data")
os.chdir("data")

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
    title = result['_source']['title'];
    links = {}
    for identifier in result['_source']['identifiers']:
        if "http" in identifier:
            print ("Getting links for identifer: ", identifier)
            links = scrape.get_content_urls_from_html_page(identifier,"curate.nd.edu")
            print("Links Found are: ", links)
            
            if links:
                link_list = thresh.prepare_link_data(links)
                identifier_directory = slugify(title + "_" + identifier)
                filename = identifier_directory + ".csv"
                
                downloaded_link_list = []
                
                for link in link_list:
                    content_filename = None
                    try:
                        print("downloading file from: ", link['content-link'])
                        content_filename = thresh.download_content_file(identifier_directory,link['content-link'])
                        print(" downloaded file: ", content_filename)
                    except:
                        content_filename = None
                    
                    if content_filename is None:
                        content_filename = "Failed to download"
                    
                    link['filename'] = content_filename
                    downloaded_link_list.append(link)

                thresh.create_manifest(identifier_directory,filename,downloaded_link_list)
                print ("json is ", result['_source'])
                thresh.write_json_file(identifier_directory,identifier_directory+".json",result['_source'])
                #write json file
                
#TODO write JSON SHARE record to directory

#could use python wget module, but will just call wget at command line for now
#create folder for the record
#write out the json record file
#write a manifest of files to be downloaded
#write each file

# call query_share
# get list of records
# grab identifiers from records
# get content links for each record
# download content for each record
