import os
import csv

#opens the top 50 most common domain files for english and spanish

with open("commonEngdomains.csv",'r') as file:
    csv_reader = csv.reader(file)
    english = list(csv_reader)


with open("commonSpdomains.csv") as file:
    csv_reader = csv.reader(file)
    spanish = list(csv_reader)
    




#writes new csv for all domains that are in the intersection between english and spanish and prints the amount of certain types of links 
with open("commonlinks.csv","w",newline="") as inF:
    writer = csv.writer(inF)

    writer.writerow(["Domain","Url","Url occurences","Common?","Language"])
    pdf = 0
    gov = 0
    org = 0
    cpdf = 0
    cgov = 0
    corg = 0
    youtube = 0
    social = 0
    for row in english:
        if 'cnn' in row[0]:
            row.append("English")
            writer.writerow(row)
            if '.pdf' in row[1]:
                cpdf +=1
            if '.gov' in row[0]:
                cgov +=1
            if '.org' in row[0]:
                corg +=1
        if 'wiki' in row[0]:
            row.append("English")
            writer.writerow(row)
            if '.pdf' in row[1]:
                cpdf +=1
            if '.gov' in row[0]:
                cgov +=1
            if '.org' in row[0]:
                corg +=1
        if 'nycvotes' in row[0]:
            row.append("English")
            writer.writerow(row)
            if '.pdf' in row[1]:
                cpdf +=1
            if '.gov' in row[0]:
                cgov +=1
            if '.org' in row[0]:
                corg +=1
        if row[3] == 'yes':
            row.append("English")
            writer.writerow(row)
            if '.pdf' in row[1]:
                cpdf +=1
            if '.gov' in row[0]:
                cgov +=1
            if '.org' in row[0]:
                corg +=1
        if '.pdf' in row[1]:
            pdf +=1
        if '.gov' in row[0]:
            gov +=1
        if '.org' in row[0]:
            org +=1
        if 'youtube' in row[1]:
            youtube +=1
        if row[0] == '':
            social +=1
    print("PDF links appear ",pdf," times in English")
    print(".gov domains appear ",gov," times in English")
    print(".org domains appear ",org," times in English")
    print("PDF links appear ",cpdf," times in English common links")
    print(".gov domains appear ",cgov," times in English common links")
    print(".org domains appear ",corg," times in English common links")
    print("YouTube links appear ",youtube," times in English")
    print("Social Media links appear ",social," times in English")
    
    pdf = 0
    gov = 0
    org = 0
    cpdf = 0
    cgov = 0
    corg = 0
    youtube = 0
    social = 0
    for row in spanish:
        if 'cnn' in row[0]:
            row.append("Spanish")
            writer.writerow(row)
            if '.pdf' in row[1]:
                cpdf +=1
            if '.gov' in row[0]:
                cgov +=1
            if '.org' in row[0]:
                corg +=1
        if 'wiki' in row[0]:
            row.append("Spanish")
            writer.writerow(row)
            if '.pdf' in row[1]:
                cpdf +=1
            if '.gov' in row[0]:
                cgov +=1
            if '.org' in row[0]:
                corg +=1
        if 'nycvotes' in row[0]:
            row.append("Spanish")
            writer.writerow(row)
            if '.pdf' in row[1]:
                cpdf +=1
            if '.gov' in row[0]:
                cgov +=1
            if '.org' in row[0]:
                corg +=1
        if row[3] == 'yes':
            row.append("Spanish")
            writer.writerow(row)
            if '.pdf' in row[1]:
                cpdf +=1
            if '.gov' in row[0]:
                cgov +=1
            if '.org' in row[0]:
                corg +=1
        if '.pdf' in row[1]:
            pdf +=1
        if '.gov' in row[0]:
            gov +=1
        if '.org' in row[0]:
            org +=1
        if 'youtube' in row[1]:
            youtube +=1
        if row[0] == '':
            social +=1
    print("PDF links appear ",pdf," times in Spanish")
    print(".gov domains appear ",gov," times in Spanish")
    print(".org domains appear ",org," times in Spanish")
    print("PDF links appear ",cpdf," times in Spanish common links")
    print(".gov domains appear ",cgov," times in Spanish common links")
    print(".org domains appear ",corg," times in Spanish common links")
    print("YouTube links appear ",youtube," times in Spanish")
    print("Social media links appear ",social," times in Spanish")
    
    



