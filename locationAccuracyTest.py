import os
import csv
import requests
from collections import Counter
from urllib.parse import urlparse


# extract information about the commonFiles and the domains that are about information outside the US

              
#list of non US ccTLDs
# 
 nonUsTld = {
    "mx", "cl", "br", "ar", "es", "fr", "de", "uk", "ca", "it", "nl", "ru", "cn", "jp", "kr", "au", "in"
}

def getTld(domain):
         parts = domain.split(".")
     if len(parts) > 1:
        return parts[-1].lower() #this will return the last part of the domain name
    
    return "" #if the domain is invalid, return an empty string


#using requests using WHOIS API for faster lookups

domains = [] 

externalDomains = []

for inputFile in inputFiles:
         with open(inputFile, "r", newline="") as f: 
         reader = csv.DictReader(f)
         next(reader) #skip the header

         for row in reader:
            getQuery = row["query"]          
            getLink = row["url"]
            getDomain = row["domain"]

            tld = getTld(domain)

            if tld in nonUsTld:
               queryLocation = tld
            else:
                #call other function
                ipLocation(getQuery)
                queryLocation 
              

            if tld in nonUsTld:
                externalDomains.append(row)



with open("externalDomains.csv", "w", newline="") as f:
     writer = csv.writer(f)
     writer.writerow(["Query", "Domain", "Link ","Country"])
     writer.writerows(externalDomains)


def ipLocation(url):

    for domain in domains: 
        url= f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_8qdMuf0whxXYIP4HhAma3qxuO3isU&domainName={domain}&outputFormat=JSON"
        response = requests.get(url)
        data = response.json()

        try: 
            country = data.get("WhoisRecord").get("registrant").get("country", "Unknown")
            print(f"Domain: {domain}, Country: {country}")

        except Exception as e:
            print(f"Error processing domain {domain}: {e}")
