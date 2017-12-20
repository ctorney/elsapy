
import pandas as pd
import numpy as np
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
df = pd.read_csv('author_ids.csv') 
df['use']=0

N = np.max(df['uid'].values) + 1


adj = np.zeros((N,N))



for index, author in df.iterrows():
    auth_srch = ElsSearch(str(author.aid),'author',coauthor=True)
    auth_srch.execute(client)
    print (author.lastname, "has", len(auth_srch.results), "collaborators found.")
    alist = ''
    for i in range(len(auth_srch.results)):
        try:
            alist = alist+auth_srch.results[i]['dc:identifier']+':'
        except:
            continue
    for i2, a2 in df.iterrows():
        if author.uid!=a2.uid:
            if alist.find(str(a2.aid))!=-1:
                adj[author.uid][a2.uid]=1
                adj[a2.uid][author.uid]=1
                print(author.lastname,'has collaborated with',a2.lastname)
                df['use'].iloc[index]=1


df.to_csv('author_ids.csv') 
            

np.save('network.npy',adj)

