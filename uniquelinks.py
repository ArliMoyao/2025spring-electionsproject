import os
import csv


#opens English and Spanish files
with open('englishDomains.csv') as inF:
    english = list(csv.DictReader(inF))
 

with open('spanishDomains.csv') as inF:
    spanish = list(csv.DictReader(inF))

from urllib.parse import urlparse

#adds fixed domains to the dictionaries
fixedEng = []
for entry in english:
    entry['fixedDomain'] = urlparse(entry['Domain']).netloc
    if not entry['fixedDomain']:
        entry['fixedDomain'] = entry['Article Link'].split('/')[2]
    fixedEng.append(entry)

fixedSp = []
for entry in spanish:
    entry['fixedDomain'] = urlparse(entry['Domain']).netloc
    if not entry['fixedDomain']:
        entry['fixedDomain'] = entry['Article Link'].split('/')[2]
    fixedSp.append(entry)



#counts the most common domains from fixed Domains
from collections import Counter
count = []
count = Counter([row['fixedDomain'] for row in fixedSp]).most_common(50)


counte = []
counte = Counter([row['fixedDomain'] for row in fixedEng]).most_common(50) 

#finds the intersection domains between English and Spanish
domainEng = set([item[0] for item in counte])
domainSp = set([item[0] for item in count])
common=[]
common = domainEng.intersection(domainSp)
print(len(common))

#creates the first row of the csv
table = [
    ["Domain","Url","Url occurences","Common?","Domain Type"]
]

#writes a list of lists for the english csv including new information for all of the links from the top 50 domains
with open ("us-news-domains-v2.0.0.csv","r",newline="") as f:
        newslinks = list(csv.DictReader(f))
new = []
for dom in domainEng:
    counted = Counter([row['Article Link'] for row in fixedEng if row['fixedDomain'] == dom])
    for c in counted:
        new.append(dom)
        new.append(c)
        new.append(counted[c])
        if dom in common:
            new.append("yes")
        else:
            new.append("no")
        if ".gov" in dom or "ma.us" in dom or "co.us" in dom or "tx.us" in dom or "ncsl" in dom:
            new.append("Government")
        if "bexar" in dom:
            new.append("County")
        if "youtube" in dom:
            new.append("Social Media")
        if "facebook" in dom:
            new.append("Social Media")
        for line in newslinks:
            if line['domain'] in dom:
                new.append("News")
        if "kff" in dom or "wikipedia" in dom or "vote.org" in dom or "usvotefoundation" in dom or "ballotpedia" in dom:
            new.append("Nonprofit")
        if "vote411" in dom or "nycvotes" in dom or "270" in dom:
            new.append("Organization")
        table.append(new)
        new = []

#writes a list of lists for the Spanish csv including new information for all of the links from the top 50 domains
tableS = [
    ["Domain","Url","Url occurences","Common?", "Domain Type"]
]
newS = []
for dom in domainSp:
    counted = Counter([row['Article Link'] for row in fixedSp if row['fixedDomain'] == dom])
    for c in counted:
        newS.append(dom)
        newS.append(c)
        newS.append(counted[c])
        if dom in common:
            newS.append("yes")
        else:
            newS.append("no")
        tableS.append(newS)
        if ".gov" in dom or "ma.us" in dom or "co.us" in dom or "tx.us" in dom or "ncsl" in dom:
            newS.append("Government")
        if  "bexar" in dom  or "harris" in dom or "ocf" in dom or "epc" in dom or "sdvote" in dom or "sbcounty" in dom:
            newS.append("County")
        if "youtube" in dom:
            newS.append("Social Media")
        if "facebook" in dom or "instagram" in dom:
            newS.append("Social Media")
        for line in newslinks:
            if line['domain'] in dom:
                newS.append("News")
        if "yahoo" in dom or "infobae" in dom or "voz" in dom or "us.as" in dom:
            newS.append("News")
        if "kff" in dom or "wikipedia" in dom or "vote.org" in dom or "brennan" in dom or "ballotpedia" in dom or "calmatters" in dom:
            newS.append("Nonprofit")
        if "vote411" in dom or "nycvotes" in dom or "270" in dom:
            newS.append("Organization")
        if ".mx" in dom:
            newS.append("Mexico")
        if "amazon" in dom:
            newS.append("Commercial")
        if ".cl" in dom:
            newS.append("Chile")
        tableS.append(newS)
        newS = []

#writes new csvs for english and spanish from the lists of lists
with open("commonEngdomains.csv","w",newline="") as file:
    writer = csv.writer(file)
    writer.writerow(table[0])

    for row in table[1:]:
        writer.writerow(row)

with open("commonSpdomains.csv","w",newline="") as file:
    writer = csv.writer(file)
    writer.writerow(tableS[0])

    for row in tableS[1:]:
        writer.writerow(row)


        

    



















    
