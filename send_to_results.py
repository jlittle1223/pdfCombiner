# -*- coding: utf-8 -*-


def send_to_results(*args):
    try:   
        from pdfCombiner import get_all_pdfs, get_unique_path, result_directory_name
        
        
    except Exception as e:
        print(e)
        input()

if __name__ == "__main__":
    import sys
    
    send_to_results(*sys.argv)