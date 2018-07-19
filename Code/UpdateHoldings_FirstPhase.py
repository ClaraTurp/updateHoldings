## 2018-07-06 Clara Turp, for McGill University Library.


import csv
import re
import string


###################
#    Functions
###################

#Functions that read files
def readTextFile(fileName):
    myFile = open(fileName, "r", encoding = "utf-8", errors = "ignore")
    reader = myFile.read()

    return reader

def readCsvFile(fileName):
    myFile = open(fileName, "r", encoding = "utf-8", errors = "ignore")
    reader = csv.reader(myFile)

    return reader


#Functions that clean strings.
def CleanString(myString):
    import string
    cleanedString = myString.lower()
    translator = cleanedString.maketrans('', '', string.punctuation)
    cleanedString = cleanedString.translate(translator)
    cleanedString = cleanedString.strip()
    cleanedString = cleanedString.rstrip()
    return cleanedString

def CleanOCN(myString):
    OCN = myString.replace("ocn", "")
    OCN = OCN.replace("on", "")
    OCN = OCN.replace("ocm", "")
    OCN = OCN.replace("\\", "")
    return OCN


#Functions that transfers text from a file to an array.
def transferEIsbnComments(myArray):
    isbnComments = []

    reader = readTextFile("EIsbnComments.txt")
    isbnComments = reader.split("\n")
    for currentComment in isbnComments:
        cleanedComment = CleanString(currentComment)
        if cleanedComment not in myArray:
            myArray.append(cleanedComment)


def transferSubscriptions(ocnArray, titleArray):
    reader = readCsvFile("subscriptions_allTitles_Final.csv")
    for row in reader:
        ocnArray.append(row[1])
        titleArray.append(row[2])

#Functions that treat exceptions
def treatIsbnNotSeparatedBySlashes(myString):
    exceptionIsbn = myString.split("$")
    if len(exceptionIsbn) > 1:
        for currentIsbn in exceptionIsbn:
            if currentIsbn[0].isdigit():
                myString = currentIsbn
            elif currentIsbn[0] == "a":
                myString = currentIsbn[1:]
    return myString


def treatCommentsWithoutSubfields(myIsbnString, isbnCommentsArray) :
    isbnToKeep = False

    isbnArray = myIsbnString.split(" ")
    
    if len(isbnArray[0]) > 12 :
        if len(isbnArray[1]) < 2:
            isbnToKeep = True
        else:
            for currentString in isbnArray :
                cleanedString = CleanString(currentString)
                if cleanedString in isbnCommentsArray:
                    isbnToKeep = True

    return isbnToKeep

#Function that updates the appropriate arrays.
def updateArray(myIsbnString, oclcNum, title, myResultArray, errorCheckingArray):
    if myIsbnString[-1] == ";":
        myIsbnString = myIsbnString[:-1]

    if len(errorCheckingArray) < 2:
        errorCheckingArray.append(myIsbnString)
    else:
        myResultArray.append([oclcNum, myIsbnString, title])            

# Function to create the files where results will be uploaded.
def createPrintFiles(filename):
    myFile = open(filename, "w", newline = "", encoding="utf-8", errors= "ignore")
    writer = csv.writer(myFile)

    return writer

###################
#    Main Code   
###################

finalComments = []

subsOcn = []
subs245 = []
SubscriptionArray = []

myResultArray = []
myErrorArray = []

transferEIsbnComments(finalComments)
transferSubscriptions(subsOcn, subs245)

mainFileReader = readCsvFile("filename.csv")
for row in mainFileReader:
    OCN = CleanOCN(row[0])
    #Remove all subscriptions:
    if OCN in subsOcn:
        SubscriptionArray.append(row)
    elif row[2] in subs245:
        SubscriptionArray.append(row)

    else:
        # errorCheckingArray allows me to find the cases when no ISBN is kept (if the array's length remains less than 2)
        errorCheckingArray = []
       
        oclcNumRow = row[0]
        errorCheckingArray.append(oclcNumRow)

        title245Row = bytes(row[2], 'utf-8').decode('utf-8','ignore')

        isbnRow = row[1].split("\\\\")

        for iteration in isbnRow:
            #Remove the empty strings. Each iteration contains MARC subfields, the ISBN ($a), and comments ($q)
            if len(iteration) > 1:
                #Finds the isbn rows that contain a subfield a ($a), which is for the valid ISBN
                isbnField = iteration.split("$a")
                for iter in isbnField:
                    #If the length = 1, it means the ISBN is subfield z which is for invalid or canceled ISBN
                    if len(iter) > 1 and iter[0][0] != "$":
                        #the subfield q ($q) is for qualifying information.
                        isbnandComment = iter.split("$q")
                        isbn = isbnandComment[0]

                        #if there is no comment ($q)
                        if len(isbnandComment) == 1:
                            #Deal with exceptions
                            isbn = treatIsbnNotSeparatedBySlashes(isbn)
                            if isbn.isdigit() and len(isbn) > 12 :
                                updateArray(isbn, oclcNumRow, title245Row, myResultArray, errorCheckingArray)
                            else:
                                if " " in isbn:
                                    isbnToKeep = treatCommentsWithoutSubfields(isbn, finalComments)
                                    if isbnToKeep == True :
                                        isbn = isbn.split(" ")[0]
                                        updateArray(isbn, oclcNumRow, title245Row, myResultArray, errorCheckingArray)
                                else:
                                    if len(isbn) > 12:
                                        updateArray(isbn, oclcNumRow, title245Row, myResultArray, errorCheckingArray)

                        #if there is a comment ($q), match with comments from the finalComments array.
                        else:
                            #look if there is a comment in $a in addition to $q
                            if not isbn.isdigit():
                                splitIsbn = isbn.split(" ")
                                if splitIsbn[0].isdigit():
                                    isbn = splitIsbn[0]
                                #Look if there is two ISBN instead of one, not separated by ///
                                elif "$" in isbn:
                                    splitIsbn = isbn.split("$")
                                    if splitIsbn[0].isdigit():
                                        isbn = splitIsbn[0]
                                    
                            if len(isbn) > 12:
                                comment = CleanString(isbnandComment[1])
                                if comment in finalComments:
                                    updateArray(isbn, oclcNumRow, title245Row, myResultArray, errorCheckingArray)
                            
        errorCheckingArray.append(row[2])
        if len(errorCheckingArray) < 3 :
            myErrorArray.append(errorCheckingArray)
        else:
            myResultArray.append(errorCheckingArray)


writer = createPrintFiles("1_FirstResults.csv")
for row in myResultArray:
    writer.writerow(row)

if len(myErrorArray) > 0:
    errorWriter = createPrintFiles("1_ErrorFirstPhase.csv")
    for line in myErrorArray:
        errorWriter.writerow(line)

if len(SubscriptionArray) > 0:
    subsWriter = createPrintFiles("1_Subscriptions.csv")
    for row in SubscriptionArray:
        subsWriter.writerow(row)
