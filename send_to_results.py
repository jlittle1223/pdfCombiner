# -*- coding: utf-8 -*-
import os
import shutil
from pdfCombiner import get_unique_path

def send_file_to_results(arg_dict, abs_file_path, abs_out_path):
    abs_in_path, filename = os.path.split(abs_file_path)
    
    split_filename = filename.split('.')
    
    if len(split_filename) == 0:
        raise ValueError("Error: Empty filename in "+abs_file_path)
    elif len(split_filename) == 1:
        result_prefix = split_filename[0]
        extension = ""
    else:
        result_prefix = ".".join(split_filename[:-1])
        extension = "."+split_filename[-1]
        
    result_path = get_unique_path(abs_out_path, result_prefix, extension)
    shutil.move(abs_file_path, result_path)
    
def send_to_results(*args):
    try:   
        from pdfCombiner import get_all_abs_pdf_paths, get_arg_dict, \
            get_abs_in_path, get_abs_out_path
        
        arg_dict = get_arg_dict(args)
        abs_in_path = get_abs_in_path(arg_dict)
        abs_pdf_paths = get_all_abs_pdf_paths(abs_in_path)
        numFiles = len(abs_pdf_paths)
        
        assert numFiles > 0, "Error: No .pdf files found in "+abs_in_path
        
        abs_out_path = get_abs_out_path(arg_dict)
        os.makedirs(abs_out_path, exist_ok=True)
        
        for abs_pdf_path in abs_pdf_paths:
            send_file_to_results(arg_dict, abs_pdf_path, abs_out_path)
    except Exception as e:
        print(e)
        input()

if __name__ == "__main__":
    import sys
    
    send_to_results(*sys.argv)