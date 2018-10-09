# -*- coding: utf-8 -*-
try:
    import os
    from PyPDF2 import PdfFileWriter, PdfFileReader
    from send_to_results import get_result_prefix_and_extension
    from pdfCombiner import get_all_abs_pdf_paths, get_arg_dict, \
            get_abs_in_path, get_abs_out_path, get_unique_path, \
            get_open_pdf_when_removing_pages, get_minimum_pages_for_removing
    from send2trash import send2trash

    def get_pages_to_remove(user_input):
        split_user_input = user_input.split(" ")
        pages_to_remove = set()
        
        for page_candidate in split_user_input:
            page_candidate = page_candidate.strip()
            
            if len(page_candidate) > 0:
                page_one_indexed = int(page_candidate)
                page = page_one_indexed - 1                 #Convert to zero-indexed
                
                assert page >= 0, "{} is less than 1, the first page".format(page_one_indexed)
                
                pages_to_remove.add(page)
            
        return pages_to_remove
    
    def try_opening(file_path):
        if " " in file_path:
            file_path = "\""+file_path+"\""
        
        try:
            try:
                #os.system("start "+file_path)              #Windows
                os.startfile(file_path)                     #Windows
            except Exception:
                os.system("open "+file_path)                #Mac OS/X (untested)
        except Exception as e:
            print("Unable to open "+file_path+", "+str(e))
    
    def remove_pdf_pages(arg_dict, abs_pdf_path):
        pdf_reader = PdfFileReader(abs_pdf_path, 'rb')
        num_pages = pdf_reader.getNumPages()
        
        abs_out_path = get_abs_out_path(arg_dict)
        min_pages = get_minimum_pages_for_removing(arg_dict)
        
        if num_pages < min_pages:
            print("{} has less than {} pages, skipping...".format(abs_pdf_path, min_pages))
            return None
        
        if get_open_pdf_when_removing_pages(arg_dict):
            try_opening(abs_pdf_path)
        
        result_prefix, extension = get_result_prefix_and_extension(abs_pdf_path)
        result_path = get_unique_path(abs_out_path, result_prefix, extension)
        
        user_input = input(("What pages do you want to remove from {}? "+
                           "(numbers separated by spaces) ").format(abs_pdf_path))
        
        pages_to_remove = get_pages_to_remove(user_input)
        
        if len(pages_to_remove) <= 0:
            return None
        
        pdf_writer = PdfFileWriter()
        
        for page in pages_to_remove:
            page_one_indexed = page + 1
            
            assert page < num_pages, ("{} is more than the number"+ \
                    " of pages, {}").format(page_one_indexed, num_pages)
        
        for i in range(num_pages):
            if i not in pages_to_remove:
                page = pdf_reader.getPage(i)
                pdf_writer.addPage(page)
                
        os.makedirs(abs_out_path, exist_ok=True)
        
        with open(result_path, 'wb') as out_handle:
            pdf_writer.write(out_handle)
            
        send2trash(abs_pdf_path)
    
    def remove_pages(*args):
        arg_dict = get_arg_dict(args)
        abs_in_path = get_abs_in_path(arg_dict)
        abs_pdf_paths = get_all_abs_pdf_paths(abs_in_path)
        numFiles = len(abs_pdf_paths)
        
        assert numFiles > 0, "Error: No .pdf files found in "+abs_in_path
        
        for abs_pdf_path in abs_pdf_paths:
            remove_pdf_pages(arg_dict, abs_pdf_path)
    
    if __name__ == "__main__":
        import sys
        
        remove_pages(*sys.argv)
except Exception as e:
    print(e)
    input()