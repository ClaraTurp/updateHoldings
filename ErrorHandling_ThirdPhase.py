import csv
import string

stopWords = ["AND", "A", "AN", "&", "THE", "OF", "FOR"]
marcSymbolArray = ["$", "/", ":", ";"]

#Keep only up to 4 words of the title for all titles returned from GOBI.
gobiArray = []
gobiListFile = open("gobi_list.csv", "r", encoding = "utf-8", errors = "ignore")
reader = csv.reader(gobiListFile)
for row in reader:
    titleWords = ""
    wordCount = 0
    if len(row[0]) > 0:
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

        if titleWords not in gobiArray:
            gobiArray.append(titleWords)

#Keep only up to 4 words of the title for all titles from the original file.
oriArray = []
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

    if titleWords not in oriArray:
        oriArray.append(titleWords)

#Sort both arrays (mostly for readability purposes)
oriArray = sorted(oriArray)
gobiArray = sorted(gobiArray)

#If the transformed title from GOBI doesn't match any transformed titles from the original list, print in error file.
printFile = open("3_ErrorsTitleMatch.txt", "w")
for instance in gobiArray:
    if instance not in oriArray:
        printFile.write(instance+ "\n")
