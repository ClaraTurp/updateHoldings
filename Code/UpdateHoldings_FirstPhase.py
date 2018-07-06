## 2018-07-06 Clara Turp, for McGill University Library.

###################
#    Functions
###################

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


###################
#    Main Code   
###################

import csv
import re
import string

isbnComments = []
finalComments = []
commentFile = open("EIsbnComments.txt", "r", encoding = "utf-8")
reader = commentFile.read()
isbnComments = reader.split("\n")
for currentComment in isbnComments:
    cleanedComment = CleanString(currentComment)
    if cleanedComment not in finalComments:
        finalComments.append(cleanedComment)
print(finalComments)
commentFile.close()

subsOcn = []
subs245 = []
subscriptionFile = open("subscriptions_allTitles_Final.csv", "r", encoding = "utf-8")
reader = csv.reader(subscriptionFile)
for row in reader:
    subsOcn.append(row[1])
    subs245.append(row[2])

    
myArray = []
myErrorArray = []
SubscriptionArray = []

with open("CurrentBatch.csv", "r", encoding = "utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        
        OCN = CleanOCN(row[0])
        if OCN in subsOcn:
            SubscriptionArray.append(row)
        elif row[2] in subs245:
            SubscriptionArray.append(row)
            
        else:
            secondLevelArray = []
            anotherArray = []
            secondLevelArray.append(row[0])
            row[2] = bytes(row[2], 'utf-8').decode('utf-8','ignore')
            
            # row[1] = the column with the ISBN. Each ISBN is separated by \\
            u = row[1].split("\\\\")
            
            for isbn in u:
                if len(isbn)> 1 :
                    isbn1 = isbn.split("$a")
                    for iteration in isbn1:
                        justIsbn = False
                        if len(iteration) > 1 and iteration[0][0] != "$":
                            isbn2 = iteration.split("$q")
                            
                            
                            # If there is no $q
                            if len(isbn2) == 1:
                             # Check if ISBN were not separated by \\
                                exceptionIsbn = isbn2[0].split("$")
                                if len(exceptionIsbn) > 1:
                                    for currentIsbn in exceptionIsbn:
                                        if currentIsbn[0].isdigit():
                                            isbn2[0] = currentIsbn
                                        elif currentIsbn[0] == "a":
                                            isbn2[0] = currentIsbn[1:]
                                            
                                # See if there are letters with regular expressions.
                                if re.search("[a-zA-Z]", isbn2[0]):
                                    isbn3 = isbn2[0].split(" ")
                                    # If there are spaces, the letters are comments added without $q
                                    if len(isbn3) > 1 :
                                        if len(isbn3[0]) > 12 :
                                            for currentString in isbn3 :
                                                if currentString in isbnComments:
                                                    if len(secondLevelArray) < 2:
                                                        secondLevelArray.append(isbn3[0])
                                                    else:
                                                        anotherArray.append(row[0])
                                                        anotherArray.append(isbn3[0])
                                                        anotherArray.append(row[2])

                                                    if len(anotherArray) == 3:
                                                        myArray.append(anotherArray)
                                                        anotherArray = []
                                                        
                                    # If there are no spaces, it's an ISBN with a final x
                                    else:
                                        if len(isbn2[0]) > 12:
                                            if isbn3[0][-1] == ";":
                                                isbn3[0] = isbn3[0][:-1]
                                                if len(secondLevelArray) < 2:
                                                    secondLevelArray.append(isbn3[0])
                                                else:
                                                    anotherArray.append(row[0])
                                                    anotherArray.append(isbn3[0])
                                                    anotherArray.append(row[2])
                                                if len(anotherArray) == 3:
                                                    myArray.append(anotherArray)
                                                    anotherArray = []
                                            else:
                                                if len(secondLevelArray) < 2:
                                                    secondLevelArray.append(isbn2[0])
                                                else:
                                                    anotherArray.append(row[0])
                                                    anotherArray.append(isbn2[0])
                                                    anotherArray.append(row[2])

                                                if len(anotherArray) == 3:
                                                    myArray.append(anotherArray)
                                                    anotherArray = []

                                #if it's only numbers:
                                elif len(isbn2[0]) > 12:
                                    if isbn2[0][-1] == ";":
                                        isbn2[0] = isbn2[0][:-1]
                                        if len(secondLevelArray) < 2:
                                            secondLevelArray.append(isbn2[0])
                                        else:
                                            anotherArray.append(row[0])
                                            anotherArray.append(isbn2[0])
                                            anotherArray.append(row[2])
                                        if len(anotherArray) == 3:
                                            myArray.append(anotherArray)
                                            anotherArray = []
                                    else:
                                        if len(secondLevelArray) < 2:
                                            secondLevelArray.append(isbn2[0])
                                        else:
                                            anotherArray.append(row[0])
                                            anotherArray.append(isbn2[0])
                                            anotherArray.append(row[2])
                                        if len(anotherArray) == 3:
                                            myArray.append(anotherArray)
                                            anotherArray = []

                                            
                            #if there is a $q, match the comment.
                            else:
                                #look if there are comment in $a in addition to $q
                                if not isbn2[0].isdigit():
                                    splitIsbn2 = isbn2[0].split(" ")
                                    if splitIsbn2[0].isdigit():
                                        isbn2[0] = splitIsbn2[0]
                                        
                                #Transfer arrays according to comments.        
                                if len(isbn2[0]) > 12:
                                    comment = CleanString(isbn2[1])
                                    if comment in finalComments:
                                        if len(tempArray) < 2:
                                            tempArray.append(isbn2[0])
                                        else:
                                            anotherArray.append(row[0])
                                            anotherArray.append(isbn2[0])
                                            anotherArray.append(row[2])

                                    if len(anotherArray) == 3:
                                        myArray.append(anotherArray)
                                        anotherArray = []

            secondLevelArray.append(row[2])
            if len(secondLevelArray) < 3 :
                myErrorArray.append(secondLevelArray)
            else:
                myArray.append(secondLevelArray)
f.close()

myFile = open("1_FirstResults.csv", "w", newline = "", encoding="utf-8", errors= "ignore")
with myFile:
    writer = csv.writer(myFile)
    for row in myArray:
        writer.writerow(row)
myFile.close()


with open('1_ErrorFirstPhase.txt','w', encoding = "utf-8") as myErrorFile:
    if len(myErrorArray) > 0:
        for line in myErrorArray:
            for instance in line:
                myErrorFile.write(instance + "\t")
            myErrorFile.write("\n")
myErrorFile.close()

myFile = open("1_Subscriptions.csv", "w", newline = "", encoding="utf-8", errors= "ignore")
with myFile:
    writer = csv.writer(myFile)
    for row in SubscriptionArray:
        writer.writerow(row)
myFile.close()

