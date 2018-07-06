## 2018-07-06 Clara Turp, for McGill University Library.

import csv
resultIsbnList = []
errorGobiIsbn = []
errors = []
goodOnes = []
with open("gobi_list.csv", "r", encoding= "UTF-8") as f:
    reader = csv.reader(f)
    for row in reader:
        #Only keep ISBN for ebook titles
        if row[6] == "eBook":
            if row[5] not in resultIsbnList:
                resultIsbnList.append(row[5])
        else:
            if row[5] not in errorGobiIsbn:
                errorGobiIsbn.append(row[5])
f.close()

#Print all rejected ISBN in one file
myErrorFile = open("2_allRejected.txt", "w", encoding= "UTF-8")
with open("firstResults.csv", "r", encoding= "UTF-8", errors = "ignore") as f:
    reader = csv.reader(f)
    for row in reader:
        if row[1] in errorGobiIsbn:
            for instance in row:
                myErrorFile.write(instance + "\t")
            myErrorFile.write("\n")
            errors.append(row[0])
myErrorFile.close()
f.close()

#Print all good ISBN in another
myPrintFile = open('2_SecondPhase.txt','w', encoding= "UTF-8")
with open("firstResults.csv", "r", encoding= "UTF-8", errors = "ignore") as f:
    reader = csv.reader(f)
    for row in reader:
        if row[1] in resultIsbnList:
            for instance in row:
                myPrintFile.write(instance + "\t")
            myPrintFile.write("\n")
            goodOnes.append(row[0])
myPrintFile.close()
f.close()

#When all ISBN were rejected for one OCN, print it in this error file.
unmatchedOcn = open("2_ErrorSecondPhase.txt", "w", encoding= "UTF-8")
for i in range(0, len(errors)):
    if errors[i] not in goodOnes:
        unmatchedOcn.write(errors[i])
        unmatchedOcn.write("\n")
unmatchedOcn.close()


