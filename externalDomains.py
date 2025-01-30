import os
import csv
from collections import Counter
from urllib.parse import urlparse

# extract information about the commonFiles and the domains that are about information outside the US

#defining a set of non-US top level domains (ccTLDs)
#read most common eng and common spanish domains 
#extract the domains that are not in the US


#list of non US ccTLDs
nonUsTld = {
    "mx", "cl", "br", "ar", "es", "fr", "de", "uk", "ca", "it", "nl", "ru", "cn", "jp", "kr", "au", "in"
}

def getTld(domain):
    parts = domain.split(".")
    if len(parts) > 1:
        return parts[-1].lower() #this will return the last part of the domain name
    
    return "" #if the domain is invalid, return an empty string


#open the commonFiles.csv file

inputFiles = ["commonSpdomains.csv", "commonEngdomains.csv"]
externalDomains = []

for inputFile in inputFiles:
    with open(inputFile, "r", newline="") as f: 
        reader = csv.reader(f)
        next(reader) #skip the header

        for row in reader:
            domain = row[0] #the domain is in the first column
            tld = getTld(domain)

            if tld in nonUsTld:
                externalDomains.append(row)

with open("externalDomains.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Domain", "Url", "Url occurences", "Common?"])
    writer.writerows(externalDomains)