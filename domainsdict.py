import os
import csv
import sys

#converts csv to a dictionary of dictionaries with the domain as the key
def csv_to_dofd(csv_file):
    result = {}
    with open(csv_file,'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row['domain']
            link = row['link']
            if key not in result:
                result[key] = {'link':link, 'occurences':1}
            else:
                result[key]['occurences'] +=1
    return result
#Input CSV file
file_path = "spanishResults.csv"
dcts = csv_to_dofd(file_path)

#Output csv file
field_names = ['Domain','Article Link','Occurences']


#writing dictionary of dictionaries into a csv 
with open('spanishDomains.csv','w') as file1:
    writer = csv.DictWriter(file1,fieldnames = field_names)
    writer.writeheader()
    for domain,data in dcts.items():
        writer.writerow({
            'Domain': domain,
            'Article Link': data['link'],
            'Occurences': data['occurences']
                        })
