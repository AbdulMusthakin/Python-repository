file = open(r"GCSE Computer Science\Text Files\Reading Text Files Lesson 1\quick.txt","r")

quicktext = file.read()

print(quicktext)


file.close()

file = open(r"GCSE Computer Science\Text Files\Reading Text Files Lesson 1\shakespearequotes.txt","r")

shakespearetext = file.read()

print(shakespearetext)

file.close()
