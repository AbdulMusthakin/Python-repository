import shutil


for i in range(10):
    shutil.copy2(
        r"C:\Users\Owner\Documents\Python\Python-repository\Tests\copy.txt",
        rf"C:\Users\Owner\Desktop\copy{i}.txt",
    )
