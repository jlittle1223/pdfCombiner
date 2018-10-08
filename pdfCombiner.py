from PyPDF2 import PdfFileMerger
import os

files = os.listdir()
pdfs = []
for file in files:
    if file[-4:] == ".pdf":
        pdfs.append(file)

numFiles = len(pdfs)

assert numFiles % 2 == 0

toMerge = []

for offset in range(int(numFiles / 2)):
    
    toMerge.append(pdfs[offset])
    toMerge.append(pdfs[-(offset + 1)])


merger = PdfFileMerger()
read_handles = []

for pdf in toMerge:
	handle = open(pdf, 'rb')
	merger.append(handle)
	read_handles.append(handle)

with open('result.pdf', 'wb') as fout:
    merger.write(fout)
    fout.close()
	
for handle in read_handles:
	handle.close()

for pdf in pdfs:
    os.remove(pdf)