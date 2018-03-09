import csv
resultIsbnList = []
myIsbnList = []
errorGobiIsbn = []
myErrorArray = []
with open("batchSearchResults.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if row[6] == "eBook":
            if row[5] not in resultIsbnList:
                resultIsbnList.append(row[5])
        else:
            if row[5] not in errorGobiIsbn:
                errorGobiIsbn.append(row[5])
f.close()

fileOfUniqueIsbn = open("uniqueIsbn.csv", "r", encoding = "UTF-8")
reader = csv.reader(fileOfUniqueIsbn)
for row in reader:
    myIsbnList.append(row[1])
fileOfUniqueIsbn.close()

fileOfClothIsbn = open("onlyCloth.csv", "r", encoding = "UTF-8")
reader = csv.reader(fileOfClothIsbn)
for row in reader:
    if row[1] not in myIsbnList:
        myIsbnList.append(row[1])
fileOfClothIsbn.close()

for i in range(0, len(errorGobiIsbn)):
    if errorGobiIsbn[i] in myIsbnList:
        myErrorArray.append(errorGobiIsbn[i])



with open('printSecondPhase.txt','w') as myPrintFile:
    for line in resultIsbnList:
        myPrintFile.write(line + "\n")
myPrintFile.close()

with open('errorSecondPhase.txt','w') as myErrorFile:
    for line in myErrorArray:
        myErrorFile.write(line + "\n")
myErrorFile.close()

with open('errorsfound.txt','w') as myErrorFile:
    for line in errorGobiIsbn:
        myErrorFile.write(line + "\n")
myErrorFile.close()
