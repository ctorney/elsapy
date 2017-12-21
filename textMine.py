
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
authDF = pd.read_csv('author_mecb.csv',index_col=0) 

Alist = authDF[authDF['comm']=='me']

sendString = ''
for _,aID in Alist.iterrows():
    if len(sendString):
        sendString = sendString + '+OR+'
    sendString = sendString + 'AU-ID('+ str(aID['aid']) +')'

doc_srch = ElsSearch(sendString,'scopus')
doc_srch.execute(client, get_all = True)
# file-output.py
fj = open('me_journals.txt','w')
fw = open('me_text.txt','w')
for i in range(len(doc_srch.results)):
    try:
        print(doc_srch.results[i]['dc:title'] )
        scp_doc = AbsDoc(uri = doc_srch.results[i]['prism:url'])
        if scp_doc.read(client):
            journal = scp_doc.data['coredata']['prism:publicationName']
            fj.write(journal)
            fj.write('\n')
            fw.write(scp_doc.title)
            fw.write('\n')
            abstract=scp_doc.data['coredata']['dc:description'] 
            fw.write(abstract)
            fw.write('\n')
        else:
            print ("Read document failed.")
    except:
        continue
fj.close()
fw.close()

Alist = authDF[authDF['comm']=='cb']

sendString = ''
for _,aID in Alist.iterrows():
    if len(sendString):
        sendString = sendString + '+OR+'
    sendString = sendString + 'AU-ID('+ str(aID['aid']) +')'

print(sendString)
doc_srch = ElsSearch(sendString,'scopus')
doc_srch.execute(client, get_all = True)
# file-output.py
fj = open('cb_journals.txt','w')
fw = open('cb_text.txt','w')
for i in range(len(doc_srch.results)):
    try:
        print(doc_srch.results[i]['dc:title'] )
        scp_doc = AbsDoc(uri = doc_srch.results[i]['prism:url'])
        if scp_doc.read(client):
            journal = scp_doc.data['coredata']['prism:publicationName']
            fj.write(journal)
            fj.write('\n')
            fw.write(scp_doc.title)
            fw.write('\n')
            abstract=scp_doc.data['coredata']['dc:description'] 
            fw.write(abstract)
            fw.write('\n')
        else:
            print ("Read document failed.")
    except:
        continue
fj.close()
fw.close()
sys.exit("bye!")

Alist = authDF[authDF['comm']=='cb']

sendString = ''
papers = ''
# file-output.py
fj = open('cb_journals.txt','w')
fw = open('cb_text.txt','w')
for _,aID in Alist.iterrows():
    sendString = 'AU-ID('+ str(aID['aid']) +')'

    print(sendString)
    doc_srch = ElsSearch(sendString,'scopus')
    doc_srch = ElsSearch('AU-ID(24588214300)+OR+AU-ID(23479355600)','scopus')
    doc_srch.execute(client, get_all = True)
    for i in range(len(doc_srch.results)):
        print(doc_srch.results[i]['dc:title'] )
        try:
            if doc_srch.results[i]['dc:identifier'] in papers:
                continue
            papers = papers + doc_srch.results[i]['dc:identifier'] 
            print(doc_srch.results[i]['dc:title'] )
            scp_doc = AbsDoc(uri = doc_srch.results[i]['prism:url'])
            if scp_doc.read(client):
                journal = scp_doc.data['coredata']['prism:publicationName']
                fj.write(journal)
                fj.write('\n')
                fw.write(scp_doc.title)
                fw.write('\n')
                abstract=scp_doc.data['coredata']['dc:description'] 
                fw.write(abstract)
                fw.write('\n')
            else:
                print ("Read document failed.")
        except:
            continue
fj.close()
fw.close()
sys.exit("bye!")
