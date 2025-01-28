#!/usr/bin/env python
# coding: utf-8

# # Parsing Organic Results from SERPs, including nested results
# 
# Brooke Perreault 10/29/23

# In[36]:


# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
import os
from urllib.parse import urlparse
import json
import sys
import csv
import re
import dateutil.parser


# In[29]:


def elements(search):
    org_pos = 1
    cmpts = []
    for el in search:
        parent_class = el.find_parent().get("class")
        if parent_class is not None and "tF2Cxc" not in parent_class and 'ULSxyf' not in parent_class: # people also ask
            if el is not None: # and not el.select('[aria-level]')
                dom = el.find('cite') # check if domain exists
                link = el.find('h3').parent.get('href')  # full link
                title = el.find('h3').text  # title of result
                bolded = [tag.text for tag in el.find_all('em') + el.find_all('b')]  # bolded words in snippet
                if dom is not None:
                    domain = dom.text.split()[0]
                    dct = {'type': 'organic', 'domain': domain, 'link': link, 
                           'title': title, 'org-position': org_pos, 'bolded': bolded}
                    org_pos+=1
                    cmpts.append(dct)
                nested = el.find_all(class_="d4rhi")
                if nested:
                    for el in nested:
                        dom = el.find('cite') # check if domain exists
                        if dom is not None:
                            domain = el.find('cite').text.split()[0]  # domain
                            link = el.find('h3').parent.get('href')  # full link
                            title = el.find('h3').text  # title of result
                            bolded = [tag.text for tag in el.find_all('em') + el.find_all('b')]  # bolded words in snippet
                            dct = {'type': 'organic', 'domain': domain, 'link': link, 
                                   'title': title, 'org-position': org_pos, 'bolded': bolded}
                            cmpts.append(dct)
                            org_pos+=1
    return cmpts


# In[30]:


def parse(filepath):
    htmlText = open(filepath, 'r', encoding="utf8").read()
    soup = BS(htmlText,'html.parser')
    #     search = soup.find('div', id='search')
    search = soup.find_all(class_="MjjYud")
    if len(search) > 1:
        cmpts = elements(search)
    if len(cmpts) == 0:
        search = soup.find_all(class_="yuRUbf")
        cmpts = elements(search)
    return cmpts


# In[39]:


def main():
    """Traverse Midterm-Data-Collection and parses the SERPs, saving a JSON file per serp"""
    path = f'Midterm-Data-Collection'
    exc = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('html'):
                query = f.split('_')[0]
                (root_folder, date, serp, state, location) = tuple(root.split('/'))
                fn = os.path.join(root, f)
                try:
                    cmpts = parse(fn)
                    with open(f'midterm-data-parsed/organic/{date}/{date}--{state}--{location}--{query}.json', "w") as outfile:
                        json.dump(cmpts, outfile)
                        print(f'midterm-data-parsed/organic/{date}/{date}--{state}--{location}--{query}.json')
                except:
                    exc.append(fn)  # any files to look at
    if len(exc) > 0:
        with open(f'midterm-exception/midterm-exception.txt', 'w') as f:
            f.writelines(exc)
main()

# # Testing

# In[41]:


# parse("random_serps/Nov-03-2022-best candidates to vote for_Texas-Alice.html")


# In[42]:


# cmptsAll = []
# for root, dirs, files in os.walk("random_serps"):
#     for f in files:
#         path = os.path.join(root, f)
#         query = f.split("-")[3].split("_")[0]
#         print(f)
#         print(query)
# #         parse(path)

