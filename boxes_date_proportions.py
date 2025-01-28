import csv, os, json

def dates_election_boxes_proportion(path):
    dates = os.listdir(path)

    results = {}
    for date in dates:
        date_key = date.split('_')[1].split('.')[0]
        results[date_key] = {'Top Box': 0, 'Where To Vote':0, 'About': 0, 'Notable Dates': 0, 'How To Vote': 0}

        with open(path + '/' + date, 'r') as csvFile:
            reader = csv.reader(csvFile)
            total = 0
            for row in reader:
                total += 1
                if(total == 1): continue

                if(row[4] == '1'): results[date_key]['Top Box'] += 1
                if(row[5] == '1'): results[date_key]['Where To Vote'] += 1
                if(row[6] == '1'): results[date_key]['About'] += 1
                if(row[7] == '1'): results[date_key]['Notable Dates'] += 1
                if(row[8] == '1'): results[date_key]['How To Vote'] += 1

            total -= 1
            results[date_key]['Top Box'] /= total
            results[date_key]['Where To Vote'] /= total
            results[date_key]['About'] /= total
            results[date_key]['Notable Dates'] /= total
            results[date_key]['How To Vote'] /= total
            
    with open('election_boxes_date_results.json', 'w') as jsonFile:
        json.dump(results, jsonFile)
        