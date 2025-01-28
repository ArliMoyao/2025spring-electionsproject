import json, csv
import os, sys
import pyarrow as pa
import pyarrow.csv as py_csv
import pandas as pd
import dateutil
from collections import defaultdict, Counter

def generateRow(file, state, city, query):
    '''
    Take in json file spit out stats dictionary
    '''
    result = {'state': state, 'city': city, 'query': query, 'featured snippet': 0, 'people also ask':0, 'videos': 0, 'related searches': 0,  'images': 0, 'knowledge panel': 0, 'local results': 0, 'dictionary': 0, 'google scholar':0,  'top ads':0, 'bottom ads':0, 'hotline': 0, 'see results about': 0}
    for item in file:
        type = item['type']
        if type in ['featured snippet', 'images', 'knowledge panel', 'dictionary', 'hotline', 'google scholar']:
            result[type] += 1
        elif type == 'map':
            result['local results'] +=1
        elif type not in ['twitter results', 'organic', 'top stories', 'unknown']:
            result[type] += len(item['data']) 
    return result


def getOtherComponents():
    '''
    Accessing the json files from the orginal and reparsed folders for csv file production.
    '''
    #query, state, city comp1 comp2 comp3 ... 
    #dict {jun03:{AM:[list]}
    master_dict = defaultdict(lambda: defaultdict(list))
    queries = ['abortion statistics 2022 .gov', 'is abortion legal.in texas', 'roe v. wade', 'roe v. wade summary', 'roe v. wade (1973)', 'roe v. wade overturned', 'roe v. wade ruling', 'roe v. wade significance', 'roe v. wade (1973) summary', 'roe v. wade case brief', 'roe v. wade quimbee', 'roe v. wade us history definition', 'what happened in roe v. wade', 'what type of abortion is most commonly performed in the u.s.?', 'obergefell v. hodges']
    bad_queries = [x.split('.')[0] for x in queries] #resulting incorrect queries      
    wrong_files = ['Abortion-AllInformation.json', 'Abortion-DomainSummary.json']   
    for root, dirs, files in os.walk('Abortion-Data-Collection_json_results'):             
        for f in files:
            if (f.endswith('.json')) and (f not in wrong_files): 
                query = f.split('_')[0].strip()  
                if query not in bad_queries: #if the file isn't a product of the incorrect naming
                    print(root)
                    (root_folder, date, time, state, location) = tuple(root.split('/'))
                    city = location.split('-')[1]
                    fn = os.path.join(root, f)
                    data = json.load(open(fn))
                    dct = generateRow(data, state, city, query)                                       
                    master_dict[date][time].append(dct)
                    print(dct)
    #From the reparsed folder
    #Filename is formatted as this: {date}--{time}--{state}--{location}--{query}.json
    for root, dirs, files in os.walk('reparse'):
        for f in files:
            if (f.endswith('.json')): 
                (date, time, state, location, fn) = tuple(f.split('--'))
                query = f.replace('.json','')
                city = location.split('-')[1]
                fn = os.path.join(root, f)
                data = json.load(open(fn))  
                dct = generateRow(data, state, city, query)     
                master_dict[date][time].append(dct)
                print(dct)
    for date in master_dict.keys():
        for time in master_dict[date].keys():
            day =  dateutil.parser.parse(date).strftime("%m-%d-%y")
            with open(f'other-components/{day}-{time}-serps-components.csv', 'w') as csvFile: 
                file = master_dict[date][time]
                fieldnames = file[0].keys()           
                writer = csv.DictWriter(csvFile, fieldnames)
                writer.writeheader()
                writer.writerows(file)
                print(f'other-components/{day}-{time}-serps-components.csv')

if __name__ == "__main__":
    getOtherComponents()

