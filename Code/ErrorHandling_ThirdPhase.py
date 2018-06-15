import csv
import string

stopWords = ["AND", "A", "AN", "&", "THE", "OF", "FOR", "LE", "LA", "LES", "DU", "DES", "UN", "DAS", "UND", "DER"]
marcSymbolArray = ["$", "/", ":", ";"]

#Keep only up to 4 words of the title for all titles returned from GOBI.
gobiDictionary = {}
gobiListFile = open("gobi_list.csv", "r", encoding = "utf-8", errors = "ignore")
reader = csv.reader(gobiListFile)
for row in reader:
    titleWords = ""
    wordCount = 0
    if len(row[0]) > 0 and row[6] == "eBook":
        title = row[0].split(":")
        title = title[0]
        titleArray = title.split(" ")
        i = 0
        matchFound = False
        while i < len(titleArray) and wordCount < 4 and titleArray[i] != ":" and titleArray[i] != ";"  and not matchFound:
            if titleArray[i] not in stopWords:
                if titleArray[i][len(titleArray[i])- 1] == ";" or titleArray[i][len(titleArray[i])- 1] == ":" :
                    matchFound = True
                titleLetter = list(titleArray[i])
                myString = ""
                x = 0
                letterFound = False
                while x < len(titleLetter) and letterFound == False:
                    if titleLetter[x] not in marcSymbolArray:
                        myString = myString + titleLetter[x]
                    if titleLetter[x] in marcSymbolArray:
                        letterFound = True
                        matchFound = True
                    x = x + 1
                titleArray[i] = myString
                titleWords = titleWords + " " + titleArray[i]
                wordCount = wordCount + 1
            i = i + 1
        translator = titleWords.maketrans('', '', string.punctuation)
        titleWords = titleWords.translate(translator)
        titleWords = titleWords.strip()

        if titleWords not in gobiDictionary:
            gobiDictionary[titleWords] = [row[5], row[0]]

#Keep only up to 4 words of the title for all titles from the original file.
oriDictionary = {}
oriListFile = open("firstResults.csv", "r", encoding = "utf-8", errors = "ignore")
reader = csv.reader(oriListFile)
for row in reader:
    titleWords = ""
    oriTitle = row[2].upper()
    oriTitle = oriTitle.split("$A")
    oriTitle = oriTitle[1]
    oriTitleArray = oriTitle.split(" ")
    i = 0
    matchFound = False
    letterFound = False
    wordCount = 0
    while i < len(oriTitleArray) and wordCount < 4 and letterFound == False:
        if oriTitleArray[i][:1] == ":" :
            matchFound = True
        titleLetter = list(oriTitleArray[i])
        myString = ""
        for x in range(0, len(titleLetter)):
            if titleLetter[x] not in marcSymbolArray and letterFound == False:
                myString = myString + titleLetter[x]
            if titleLetter[x] in marcSymbolArray:
                letterFound = True
        oriTitleArray[i] = myString
        if oriTitleArray[i] not in stopWords and not matchFound:
            titleWords = titleWords + " " + oriTitleArray[i]
            wordCount = wordCount + 1

        i = i + 1
    translator = titleWords.maketrans('', '', string.punctuation)
    titleWords = titleWords.translate(translator)
    titleWords = titleWords.strip()

    if titleWords not in oriDictionary:
        oriDictionary[titleWords] = row[1]

#Create a final Dictionary where the key is the ISBN
myFinalDic = {}
for key in gobiDictionary:
    if key not in oriDictionary and gobiDictionary[key][0] not in myFinalDic:
        myFinalDic[gobiDictionary[key][0]] = gobiDictionary[key][1]

#Print the title from GOBI, the ISBN, and the original title.
isbnList = []
myPrintFile = open("3_ErrorsTitleMatch.csv", "w", newline = "", encoding="utf-8", errors= "ignore" )
writer = csv.writer(myPrintFile)
oriListFile = open("1_FirstResults.csv", "r", encoding = "utf-8", errors = "ignore")
reader = csv.reader(oriListFile)
for row in reader:
    if row[1] in myFinalDic and row[1] not in isbnList:
        isbnList.append(row[1])
        writer.writerow([myFinalDic[row[1]], row[1], row[2]])

