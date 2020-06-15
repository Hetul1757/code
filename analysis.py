# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 11:50:35 2020

@author: Admin
"""

import csv
import pandas as pd
import os
from urllib.parse import urljoin
import requests
import json
from scholarly import scholarly
import re

data = pd.read_csv('E:/BIA_660_B/SCORE_csv.csv')
API_ENDPOINT = "https://api.osf.io/v2/files"
VIEW_ONLY_KEY = "1c79efb782e54b05acd3b1aa2dd375fd"

temp = pd.DataFrame(columns={'count','references'})

def retrieve_file(url):
    guid = os.path.split(url)[-1]
    link = urljoin(API_ENDPOINT, "files/"+guid+ "?view_only=" + VIEW_ONLY_KEY)
    r = requests.get(link)
    url_download = r.json()['data']['links']['download']
    params = {'url':url_download}
    r = requests.get('https://ref.scholarcy.com/api/references/extract',params)
    x = json.loads(r.content.decode('utf-8'))
    return x

def ref_count(api_data):
    print(api_data)
    count = len(api_data['references'])
    return count
    
def ref_if(api_data):
    api_data = api_data['references']
    link_list = dict()
    for i in api_data:
        print(i)
        article_name = i
        print(re.split('\.|\?',(re.split("[0-9]{4}",i)[1]))[2])        
        journal_name = re.split('\.|\?',(re.split("[0-9]{4}",i)[1]))[2]
        link_list[article_name] = journal_name
    return link_list


    
def get_features(link):
    a = retrieve_file(link)
    b = ref_count(a)
    c = ref_if(a)
    return pd.Series((b,c))
    
        
temp[['count','references']] = data['pdf'].head(1).apply(get_features)   
        
#https://ref.scholarcy.com/api/metadata/extract
#https://osf.io/download/82j4y/?view_only=1c79efb782e54b05acd3b1aa2dd375fd
#https://scholar.google.co.uk/scholar?q=Steinel%2C%20W.%20De%20Dreu%2C%20C.K.%20Social%20motives%20and%20strategic%20misrepresentation%20in%20social%20decision%20making%202004        
    
requests.get('https://scholar.google.co.uk/scholar?q=Steinel%2C%20W.%20De%20Dreu%2C%20C.K.%20Social%20motives%20and%20strategic%20misrepresentation%20in%20social%20decision%20making%202004')




"""Test script."""
TEST_URL_XML = "https://osf.io/5wqsg/files/osfstorage/5cf1d30223fec40017f187ca"
TEST_URL_PDF = "https://osf.io/hcxdq/files/osfstorage/5cf1c86b2a50c4001880bd77"

f = retrieve_file(TEST_URL_PDF)

'''from bs4 import BeautifulSoup
soup = BeautifulSoup(f, 'html.parser')
print(str(soup), file=open("output.html", "a"))'''



#files = {'file':('C:/Users/Admin/Downloads/Mason_JournExpSocPsych_2018_AX.pdf', open('C:/Users/Admin/Downloads/Mason_JournExpSocPsych_2018_AX.pdf', 'rb'))}

params = {'url':url_download}

f = requests.post('https://ref.scholarcy.com/api/references/extract',params)

x = json.loads(f.content.decode('utf-8'))

requests.post(url, params=params)
#files = {'file':(url_download, open('url_download', 'rb'))}
from bs4 import BeautifulSoup
temp_url = 'https://scholar.google.co.uk/scholar?q=Steinel%2C%20W.%20De%20Dreu%2C%20C.K.%20Social%20motives%20and%20strategic%20misrepresentation%20in%20social%20decision%20making%202004'
r = requests.get(temp_url)
soup = BeautifulSoup(r.text,'html.parser')




try:
    print(b.bib['journal'])
except KeyError:
    print(b.bib['venue'])



