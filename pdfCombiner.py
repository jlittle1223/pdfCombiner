def get_path(parent_path, file_prefix, file_suffix, copy_index=0):
    if copy_index <= 0:
        return os.path.join(parent_path, file_prefix+file_suffix)
    else:
        return os.path.join(parent_path, file_prefix+"_"+str(copy_index)+file_suffix)

def get_unique_path(parent_path, file_prefix, file_suffix, copy_index=0):
    while True:
        candidate_path = get_path(parent_path, file_prefix, file_suffix, copy_index)
        
        if not os.path.exists(candidate_path):
            return candidate_path
        
        copy_index += 1

pdf_extension = ".pdf"
result_directory_name = "results"
result_prefix = "result"
        
def get_all_pdfs(path='.'):
    abs_path = os.path.abspath(path)
    files = os.listdir(abs_path)
    pdfs = []
    for file in files:
        if file[-4:] == pdf_extension:
            abs_file_path = os.path.join(abs_path, file)
            pdfs.append(abs_file_path)
            
    return pdfs
    

if __name__ == "__main__":
    read_handles = []
    
    try:    
        from PyPDF2 import PdfFileMerger
        from send2trash import send2trash
        import os
        import sys
        
        pdf_path = '.'
        if len(sys.argv) > 1:
            pdf_path = sys.argv[1]
    
        pdfs = get_all_pdfs(pdf_path)               
        numFiles = len(pdfs)
        abs_pdf_path = os.path.abspath(pdf_path)
        
        assert numFiles > 0, "Error: No .pdf files found in "+abs_pdf_path
        assert numFiles % 2 == 0, "Error: Encountered {} .pdf files in {}, need an even number".format(numFiles, abs_pdf_path)
        
        toMerge = []
        
        for offset in range(int(numFiles / 2)):
            toMerge.append(pdfs[offset])
            toMerge.append(pdfs[-(offset + 1)])
        
        merger = PdfFileMerger()
        
        for pdf in toMerge:
            handle = open(pdf, 'rb')
            merger.append(handle)
            read_handles.append(handle)
        
        result_directory = os.path.join(abs_pdf_path, result_directory_name)
        os.makedirs(result_directory, exist_ok=True)
        result_path = get_unique_path(result_directory, result_prefix, pdf_extension)
        
        with open(result_path, 'wb') as fout:
            merger.write(fout)
            fout.close()
        	
        for handle in read_handles:
            handle.close()
        
        read_handles.clear()
        
        for pdf in pdfs:
            send2trash(pdf)
    except Exception as e:
        for handle in read_handles:     #In case anything goes wrong
            handle.close()
        
        print(e)
        input()