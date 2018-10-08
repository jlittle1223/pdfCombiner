from PyPDF2 import PdfFileMerger
import os

pdfs = os.listdir()
for file in pdfs:
    if file[-4:] != ".pdf":
        pdfs.remove(file)

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
