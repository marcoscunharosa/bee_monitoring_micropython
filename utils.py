import os

def remove_substrings(string, substrings):
    aux_string = string
    for substring in substrings:
        aux_string = aux_string.replace(substring, '')
    
    return aux_string

def file_exists(path):
    try:
        os.stat(path)
        return True
    except OSError as e:
        print("Server manager error: ", e)
        return False
