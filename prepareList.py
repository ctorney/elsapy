import pandas as pd
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json



## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']


#open author list
df = pd.read_csv('author_list.txt',names=['lastname','firstname'])






for index, author in df.iterrows():
    
    ## Initialize author search object and execute search
    auth_srch = ElsSearch('authlast('+author.lastname+')+AUTHFIRST('+author.firstname+')','author')
    auth_srch.execute(client)
    
    lc = len(auth_srch.results)
    
    if lc==0:
        print(author.lastname, author.firstname, 'not found')
        continue
    
       
    aid = auth_srch.results[0]['dc:identifier']
    aid=aid[-11:]

    df.set_value(index,'ID',aid)
    
    if lc>1:
        print ("search returned", lc, "results.")
        for i in range(lc):
            
            print('====== option ' + str(i) +' ==========')
            aid = auth_srch.results[i]['dc:identifier']
            aid=aid[-11:]

            print(auth_srch.results[i]['preferred-name'])
            print(auth_srch.results[i]['affiliation-current'])
            print('author ID:',aid)

    
df.to_csv('author_ids.csv')

