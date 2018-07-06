## 2018-07-06 Clara Turp, for McGill University Library.

###################
#    Functions
###################

def import_titles_inArray(myArray, filename):
    title_list = open(filename, "r", encoding = "UTF-8", errors= "ignore")
    for titles in title_list:
        titles = titles.rstrip()
        myArray.append(titles)

###################
#    Main Code   
###################

commentArray = []
commentArray = []
addedAlreadyCommentArray = []
import_titles_inArray(addedAlreadyCommentArray, "EIsbnComments.txt")

file = open("comments_Gobi.txt", "r", encoding = "utf-8")
lines = file.readlines()
for line in lines:
    line = line.rstrip()
    splitLine = line.split(";")
    for iterations in splitLine :
        comment = iterations.split("$")
        for i in range (0,len(comment)):
            if len(comment[i]) > 1:
                if comment[i][0] == "q":
                    comment[i] = comment[i][1:]
                    if comment[i] not in commentArray and comment[i] not in addedAlreadyCommentArray:
                        commentArray.append(comment[i])

commentArray.sort()

file.close()
file = open("comments_Gobi_2.txt", "w", encoding = "utf-8")
for currentComment in commentArray:
    file.write(currentComment + "\n")
