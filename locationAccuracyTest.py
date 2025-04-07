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

def ipLocation(url):

    for domain in domains: 
        url= f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_8qdMuf0whxXYIP4HhAma3qxuO3isU&domainName={domain}&outputFormat=JSON"
        response = requests.get(url)
        data = response.json()

        try: 
            country = data.get("WhoisRecord").get("registrant").get("country", "Unknown")
            return(f"Domain: {domain}, Country: {country}")

        except Exception as e:
            return(f"Error processing domain {domain}: {e}")
#using requests using WHOIS API for faster lookups
domains = [] 

externalDomains = []

for inputFile in inputFiles:
         with open(inputFile, "r", newline="") as f: 
            reader = csv.DictReader(f)
         #next(reader) #skip the header
         

         for row in reader:
            domains.append(row)
            #getQuery = row["query"]          
            #getLink = row["url"]
            #getDomain = row["domain"]

            tld = getTld(row['domain'])
            if tld in nonUsTld:
               queryLocation = tld
               domains.append(tld)
               
            else:
                #call other function
                ipl = ipLocation(row['url'])
                domains.append(ipl)

         externalDomains.append(domains)
         domains = []

             



with open("externalDomains.csv", "w", newline="") as f:
     writer = csv.writer(f)
     writer.writerow(["Query", "Domain", "Link ","Country"])
     writer.writerows(externalDomains)



