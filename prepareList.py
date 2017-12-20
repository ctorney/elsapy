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
    if index<46:
        continue
    ## Initialize author search object and execute search
    auth_srch = ElsSearch('authlast('+author.lastname+')+AUTHFIRST('+author.firstname+')','author')
    auth_srch.execute(client)
    
    lc = len(auth_srch.results)
    
    if lc==0:
        print(author.lastname, author.firstname, 'not found')
        continue
    
    
    if lc==1:
        try: 
            aid = auth_srch.results[0]['dc:identifier']
            aid=aid[-11:]
            lst.append([author.lastname, author.firstname, index, aid])
        except:
            print(author.lastname, author.firstname, 'no ID')
        

    
    
    if lc>1:
        print ("search returned", lc, "results.")
        for i in range(lc):
            
            print('====== option ' + str(i) +' ==========')
            try:
                aid = auth_srch.results[i]['dc:identifier']
                aid=aid[-11:]
            except:
                print('no ID for this entry')
                continue
                
            try:
                print(auth_srch.results[i]['preferred-name'])
            except:
                print('no name for this entry')
                continue
            try:
                print(auth_srch.results[i]['affiliation-current'])
            except:
                continue
            user_entry = input("Correct entry? n: ")
            if user_entry!='n':
                lst.append([author.lastname, author.firstname, index, aid])
            
                
        print('**********************************************************')
        print('end of author',author.lastname)
        print('**********************************************************')

outDF = pd.DataFrame(lst, columns=['lastname','firstname','uid','aid'])
 
outDF.to_csv('author_ids.csv')

