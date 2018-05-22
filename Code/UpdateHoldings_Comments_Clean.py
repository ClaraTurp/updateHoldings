###############
###############


commentArray = []

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
                    if comment[i] not in commentArray:
                        commentArray.append(comment[i])

commentArray.sort()

file.close()
file = open("comments_Gobi_2.txt", "w", encoding = "utf-8")
for currentComment in commentArray:
    file.write(currentComment + "\n")
