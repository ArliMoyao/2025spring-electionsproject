#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import json
import sys


def getAllTopStories():
    allTopStories = []
    directory = 'midterm-parsed-inorganic'
#     directory = "/Users/catherinefoster/Downloads/topStories_jsons"
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('json'):
                f = os.path.join(root, filename)
                with open(f, 'r', encoding="utf8") as inFile:
                    allTopStories += json.load(inFile)
    return allTopStories


# In[ ]:


def findNews(self):
    topStoriesList = getAllTopStories()
    
    listOfDomains = []
    for topStories in topStoriesList:
        try:
            for domainDict in topStories["data"]:
                domain = domainDict["domain"]
                if domain not in listOfDomains:
                    listOfDomains.append(domain)    
        except KeyError as kEx:
            print(kEx)
            pass
        except IndexError as iEx:
            print(iEx + "\n" + topStories)
            pass
    sTopStories = pd.Series(listOfDomains)
    
    df = pd.read_csv("/credlab2022/totalOccurrences.csv");
    sOrganic = pd.Series([s.split("://")[1] for s in df["domain"]])
    
    news = pd.Series(list(set(sTopStories).intersection(set(sOrganic))))
    with pd.ExcelWriter('/credlab2022/newsDomains.xlsx') as writer:  
        news.to_excel(writer, sheet_name='sheet1')
    
    print("done")


# In[ ]:


if __name__ == '__main__':
    findNews(sys.argv[0])

