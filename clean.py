import os

files = os.listdir()
pdfs = []
for file in files:
    if file[-4:] == ".pdf" and file != "result.pdf":
        pdfs.append(file)

for pdf in pdfs:
    os.remove(pdf)
