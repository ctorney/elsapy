
import pandas as pd
import numpy as np
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json


import sys

## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']
authDF = pd.read_csv('author_ids.csv',index_col=0) 
commDF = pd.read_csv('community2.csv') 

comms = np.unique(commDF['community'].values)


authDF = authDF[authDF['use']==1]
authDF = authDF.reset_index()
authDF['comm']='na'

for commer in comms:
    cb_auth=0
    me_auth=0
    thisComm = commDF[commDF['community']==commer]

    print(commer,thisComm['lastname'])
    for _,auth in thisComm.iterrows():
        idList = authDF[authDF['lastname']==auth['lastname']]
        commString = ''

        for _,aID in idList.iterrows():
            if len(commString):

                commString = commString + '+OR'
            commString = commString + '+AU-ID('+ str(aID['aid']) +')'

#u_id(24588214300)
## Initialize doc search object and execute search, retrieving all results
#doc_srch = ElsSearch('collective+movement+ecology+AU-ID(24588214300)+AU-ID(23479355600)','scopus')
        doc_srch = ElsSearch('title("collective")+' + commString,'scopus')
        doc_srch.execute(client, get_all = True)
        cbCount = len(doc_srch.results)
 #       title("neuropsychological evidence")
        doc_srch = ElsSearch('title("ecology")+' + commString,'scopus')
        doc_srch.execute(client, get_all = True)
        meCount = len(doc_srch.results)
        print(meCount,cbCount)
        if meCount>cbCount:
            me_auth+=1
            print(auth['lastname'] + ' ME!')
        if meCount<cbCount:
            cb_auth+=1
            print(auth['lastname'] + ' CB!')

    if me_auth>cb_auth:
        authDF.loc[authDF.isin(thisComm['lastname'].values)['lastname'],'comm']='me'
        print('community ' + str(commer) + ' is ME!')
    if me_auth<cb_auth:
        authDF.loc[authDF.isin(thisComm['lastname'].values)['lastname'],'comm']='cb'
        print('community ' + str(commer) + ' is CB!')
authDF.to_csv('author_mecb.csv') 
sys.exit("bye!")
for i in range(len(doc_srch.results)):
    print(doc_srch.results[i]['dc:title'] )
authDF['comm']='na'

for commer in comms:
    thisComm = commDF[commDF['community']==commer]

    print(commer,thisComm['lastname'])
    commString = ''
    for _,auth in thisComm.iterrows():
        idList = authDF[authDF['lastname']==auth['lastname']]

        for _,aID in idList.iterrows():
            if len(commString):

                commString = commString + '+OR'
            commString = commString + '+AU-ID('+ str(aID['aid']) +')'

#u_id(24588214300)
## Initialize doc search object and execute search, retrieving all results
#doc_srch = ElsSearch('collective+movement+ecology+AU-ID(24588214300)+AU-ID(23479355600)','scopus')
    doc_srch = ElsSearch('collective+behaviour+OR+behavior+' + commString,'scopus')
    doc_srch.execute(client, get_all = True)
    cbCount = len(doc_srch.results)
    doc_srch = ElsSearch('movement+AND+ecology+' + commString,'scopus')
    doc_srch.execute(client, get_all = True)
    meCount = len(doc_srch.results)
    print(meCount,cbCount)
    if meCount>cbCount:
        authDF.loc[authDF.isin(thisComm['lastname'].values)['lastname'],'comm']='me'
        print('community ' + str(commer) + ' is ME!')
    if meCount<cbCount:
        authDF.loc[authDF.isin(thisComm['lastname'].values)['lastname'],'comm']='cb'
        print('community ' + str(commer) + ' is CB!')
authDF.to_csv('author_mecb.csv') 
sys.exit("bye!")

#u_id(24588214300)
## Initialize doc search object and execute search, retrieving all results
#doc_srch = ElsSearch('collective+movement+ecology+AU-ID(24588214300)+AU-ID(23479355600)','scopus')
doc_srch = ElsSearch('movement+ecology+AU-ID(24588214300)+OR+AU-ID(23479355600)','scopus')
doc_srch.execute(client, get_all = True)
print ("doc_srch has", len(doc_srch.results), "results.")
for i in range(len(doc_srch.results)):
    print(doc_srch.results[i]['dc:title'] )
    
    
## Scopus (Abtract) document example
# Initialize document with ID as integer
title = scp_doc.data['coredata']['prism:publicationName']
scp_doc = AbsDoc(uri = doc_srch.results[i]['prism:url'])
if scp_doc.read(client):
    print ("scp_doc.title: ", scp_doc.title)
    abstract=scp_doc.data['coredata']['dc:description'] 
    print(abstract)
else:
    print ("Read document failed.")
