file1 = open(r"GCSE Computer Science\Text Files\Reading Text Files Lesson 1\transcript1.txt","r")
file2 = open(r"GCSE Computer Science\Text Files\Reading Text Files Lesson 1\transcript2.txt","r")

for l1, l2 in zip(file1, file2):
    print(l1.strip())
    print(l2.strip())
