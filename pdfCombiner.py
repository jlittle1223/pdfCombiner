from PyPDF2 import PdfFileMerger
import os

files = os.listdir()
pdfs = []
for file in files:
    if file[-4:] == ".pdf":
        pdfs.append(file)

print(pdfs)
numFiles = len(pdfs)

assert numFiles % 2 == 0

toMerge = []

for offset in range(int(numFiles / 2)):
    
    toMerge.append(pdfs[offset])
    toMerge.append(pdfs[-(offset + 1)])


merger = PdfFileMerger()

for pdf in toMerge:
    merger.append(open(pdf, 'rb'))

with open('result.pdf', 'wb') as fout:
    merger.write(fout)
