import csv
import requests
import json

subsCollection = ["<kb:collection_uid>collection_Name</kb:collection_uid>"]

realSubscriptionTitles = []
perpetualTitles = []

mySubscriptionFile = open("test.csv", "r", encoding="utf-8", errors= "ignore")
reader = csv.reader(mySubscriptionFile)
for row in reader:
    param = "oclcnum=" + row[1]
    myKey = "&wskey=ThisIsMyKey"
    myUrl = "http://worldcat.org/webservices/kb/rest/entries/search?" + param + myKey

    response = requests.get(myUrl)
    data = response.content.decode("utf-8")

    import re
    matchFound = False
    #for m in re.findall("<kb:collection_uid>[A-Za-z0-9._-]*</kb:collection_uid>", data):
    m = 0
    allIterations = []
    allIterations = re.findall("<kb:collection_uid>[A-Za-z0-9._-]*</kb:collection_uid>", data)
    while m < len(allIterations) and matchFound == False:
        if allIterations[m] not in subsCollection :
            matchFound = True
            perpetualTitles.append(row)
        m = m + 1
    if matchFound == False:
        realSubscriptionTitles.append(row)
mySubscriptionFile.close()         
        
myFile = open("subscriptions_OcnUnmatched.csv", "w", newline = "", encoding="utf-8", errors= "ignore")
with myFile:
    writer = csv.writer(myFile)
    for row in realSubscriptionTitles:
        writer.writerow(row)
myFile.close()

myFile = open("subscriptions_alsoPerpetual.csv", "w", newline = "", encoding="utf-8", errors= "ignore")
with myFile:
    writer = csv.writer(myFile)
    for row in perpetualTitles:
        writer.writerow(row)
myFile.close()

