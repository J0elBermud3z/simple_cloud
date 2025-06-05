import os
import mimetypes


def secure_path(base_dir:str, user_input:str) -> bool:

    if user_input == '/':
        return True
    
    user_path = os.path.normpath(os.path.join(base_dir, user_input))
    if os.path.commonprefix([user_path, base_dir]) != base_dir:
        return False
    
    return True

def format_directory(directory:str) -> str:
    
    return (directory.replace('_',' ')).replace('.','')

    
def get_total_files_and_directories(path) -> int:
    
    total = 0

    for item in os.listdir(path): 
        full_path = os.path.join(path, item) 
        total += 1  

        if os.path.isdir(full_path): 
            total += get_total_files_and_directories(full_path) 

    return total

def have_files(path) -> bool:

    return (False if len(os.listdir(path)) >= 1 else True) 

def get_filetype(file) -> str:

    mime_type, _ = mimetypes.guess_type(file)
    return mime_type


def get_path_size(path) -> int:

    total_size = 0
    if os.path.isfile(path):
        return os.path.getsize(path)
    
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)

    return total_size


