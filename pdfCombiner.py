import os
from collections import OrderedDict

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
        
def get_default_abs_out_path(arg_dict):
    abs_in_path = get_abs_in_path(arg_dict)
    default_abs_out_path = os.path.join(abs_in_path, default_out_directory_name)
    
    return default_abs_out_path

pdf_extension = ".pdf"
default_out_directory_name = "results"

in_flag = '-in'
out_flag = '-out'
result_prefix_flag = '-r'
open_pdf_when_removing_pages_flag = '-o'
minimum_pages_for_removing_flag = '-min'

default_flag_values = OrderedDict()
default_flag_values[in_flag]='.'
default_flag_values[out_flag]=get_default_abs_out_path
default_flag_values[result_prefix_flag]="result"
default_flag_values[open_pdf_when_removing_pages_flag]=True
default_flag_values[minimum_pages_for_removing_flag]=3

def process_flag_candiate(flag_candidate):
    flag_candidate = flag_candidate.strip()
    flag_candidate = flag_candidate.lower()
    
    return flag_candidate

def get_arg_dict(args):
    arg_dict = {}
    i = 1
    
    for i in range(1, len(args), 2):
        arg = args[i]
        flag_candidate = process_flag_candiate(arg)
        
        assert flag_candidate in default_flag_values, "Error: Unknown flag "+arg
        
        arg_dict[flag_candidate] = args[i+1]
        
    for flag, default_value in default_flag_values.items():
        if flag not in arg_dict:
            if callable(default_value):
                arg_dict[flag] = default_value(arg_dict)
            else:
                arg_dict[flag] = default_value
            
    return arg_dict
        
def get_abs_arg_path(arg_dict, arg_flag):
    rel_arg_path = arg_dict[arg_flag]
    abs_arg_path = os.path.abspath(rel_arg_path)
    
    return abs_arg_path
        
def get_abs_in_path(arg_dict):
    return get_abs_arg_path(arg_dict, in_flag)

def get_abs_out_path(arg_dict):
    return get_abs_arg_path(arg_dict, out_flag)

def get_result_prefix(arg_dict):
    return arg_dict[result_prefix_flag]

def get_open_pdf_when_removing_pages(arg_dict):
    return arg_dict[open_pdf_when_removing_pages_flag]

def get_minimum_pages_for_removing(arg_dict):
    try:
        return int(arg_dict[minimum_pages_for_removing_flag])
    except:
        raise ValueError(("Minimum pages for removing must be an integer, "+
                          "got {}").format(arg_dict[minimum_pages_for_removing_flag]))

def get_all_abs_pdf_paths(path='.'):
    abs_path = os.path.abspath(path)
    files = os.listdir(abs_path)
    files.sort()
    abs_pdf_paths = []
    
    for file in files:
        if file[-4:] == pdf_extension:
            abs_file_path = os.path.join(abs_path, file)
            abs_pdf_paths.append(abs_file_path)
            
    return abs_pdf_paths
    
def combine_pdfs(*args):
    read_handles = []
    
    try:    
        from PyPDF2 import PdfFileMerger
        from send2trash import send2trash
        
        arg_dict = get_arg_dict(args)
        abs_in_path = get_abs_in_path(arg_dict)
        abs_pdf_paths = get_all_abs_pdf_paths(abs_in_path)
        numFiles = len(abs_pdf_paths)
        
        assert numFiles > 0, "Error: No .pdf files found in "+abs_in_path
        assert numFiles % 2 == 0, ("Error: Encountered {} .pdf files in {}, "+ \
            "need an even number").format(numFiles, abs_in_path)
        
        toMerge = []
        
        for offset in range(int(numFiles / 2)):
            toMerge.append(abs_pdf_paths[offset])
            toMerge.append(abs_pdf_paths[-(offset + 1)])
        
        merger = PdfFileMerger()
        
        for pdf in toMerge:
            handle = open(pdf, 'rb')
            merger.append(handle)
            read_handles.append(handle)
        
        abs_out_path = get_abs_out_path(arg_dict)
        os.makedirs(abs_out_path, exist_ok=True)
        
        result_prefix = get_result_prefix(arg_dict)
        result_path = get_unique_path(abs_out_path, result_prefix, pdf_extension)
        
        with open(result_path, 'wb') as fout:
            merger.write(fout)
            fout.close()
        	
        for handle in read_handles:
            handle.close()
        
        read_handles.clear()
        
        for abs_pdf_path in abs_pdf_paths:
            send2trash(abs_pdf_path)
    except Exception as e:
        for handle in read_handles:     #In case anything goes wrong
            handle.close()
        
        print(e)
        input()

if __name__ == "__main__":
    import sys
    
    combine_pdfs(*sys.argv)