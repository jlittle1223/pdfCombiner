from PyPDF2 import PdfFileMerger
import os
from send2trash import send2trash

try:
    pdf_extension = ".pdf"
    
    files = os.listdir()
    pdfs = []
    for file in files:
        if file[-4:] == pdf_extension:
            pdfs.append(file)
    
    numFiles = len(pdfs)
    
    assert numFiles > 0, "Error: No .pdf files found"
    assert numFiles % 2 == 0, "Error: Encountered {} .pdf files, need an even number".format(numFiles)
    
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
        
    result_directory = "results"
    result_prefix = "result"
    result_filename = result_prefix+pdf_extension
    result_path = os.path.join(result_directory, result_filename)
    copy_index = 1
    
    os.makedirs(result_directory, exist_ok=True)
    
    while os.path.exists(result_path):
        result_filename = result_prefix+"_"+str(copy_index)+pdf_extension
        result_path = os.path.join(result_directory, result_filename)
        copy_index += 1
    
    with open(result_path, 'wb') as fout:
        merger.write(fout)
        fout.close()
    	
    for handle in read_handles:
        handle.close()
    
    for pdf in pdfs:
        send2trash(pdf)
except Exception as e:
    print(e)
    input()