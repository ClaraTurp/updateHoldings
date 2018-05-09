import csv
import string
ebookArray = []
errorArray = []

mySubscriptionFile = open("subscriptions.csv", "r", encoding="utf-8", errors= "ignore")
reader = csv.reader(mySubscriptionFile)
for row in reader:
    if row[0][7] == "m" or row[0][7] == "i" :
        if len(row[3]) > 1:
            physicalDesc = row[3].split("$a")
            myString = physicalDesc[1]
            translator = str.maketrans(string.punctuation, " "*len(string.punctuation))
            myString = myString.translate(translator)
            onlineBook = myString.split(" ")
            for word in onlineBook:
                if word == "online" or word == "computer" or word == "electronic" or word == "Online" or word == "Computer" or word == "Electronic":
                    ebookArray.append(row)
        else:
            ebookArray.append(row)
mySubscriptionFile.close()


myFile = open("eBookSubscriptions.csv", "w", newline = "", encoding="utf-8", errors= "ignore")
with myFile:
    writer = csv.writer(myFile)
    for row in ebookArray:
        writer.writerow(row)
myFile.close()
