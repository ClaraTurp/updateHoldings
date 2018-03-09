import csv
import re

#import all possible comments in array
isbnComments = []
commentFile = open("EIsbnComments.txt", "r", encoding = "utf-8")
reader = commentFile.read()
isbnComments = reader.split("\n")
commentFile.close()

myArray = []
myErrorArray = []
with open("sample_titles.csv", "r", encoding = "utf-8") as f:
    reader = csv.reader(f)

    for row in reader:
        secondLevelArray = []
        anotherArray = []
        secondLevelArray.append(row[0])
        #Ignore non UTF-8 characters
        row[2] = bytes(row[2], 'utf-8').decode('utf-8','ignore')
        # row[1] = the column with the ISBN. Each ISBN is separated by \\
        u = row[1].split("\\\\")
        for isbn in u:
            # Remove empty strings
            if len(isbn)> 1 :
                #Split in $a
                isbn1 = isbn.split("$a")
                for iteration in isbn1:
                    justIsbn = False
                    if len(iteration) > 1 and iteration[0][0] != "$":
                        isbn2 = iteration.split("$q")
                        # If there is no $q
                        if len(isbn2) == 1:
                            # See if there are letters
                            if re.search("[a-zA-Z]", isbn2[0]):
                                isbn3 = isbn2[0].split(" ")
                                # If there are spaces
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
                            if len(isbn2[0]) > 12:
                                if isbn2[1] in isbnComments:
                                    if len(secondLevelArray) < 2:
                                        secondLevelArray.append(isbn2[0])
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

with open('printFirstPhase.txt','w', encoding = "utf-8") as myPrintFile:
    for line in myArray:
        for instance in line:
            myPrintFile.write(instance + "\t")
        myPrintFile.write("\n")
myPrintFile.close()

with open('printErrorFirstPhase.txt','w', encoding = "utf-8") as myErrorFile:
    if len(myErrorArray) > 0:
        for line in myErrorArray:
            for instance in line:
                myErrorFile.write(instance + "\t")
            myErrorFile.write("\n")
myErrorFile.close()
























#import pymarc
#from pymarc import MARCReader
#with open("test.dat", "rb") as fh:
#    reader = MARCReader(fh)
#    for record in reader:
#        print(record["020"]["z"])
        #print(record.isbn())
        #for f in record.get_fields("020"):
        #    print(f)
