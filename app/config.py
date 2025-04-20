import os 

class Config:
    
    DEBUG = False

class Paths:

    MAIN_PATH = str(os.path.abspath(__file__)).replace('/config.py','/')
    UPLOADED_FILES = os.path.join(MAIN_PATH,'uploaded_files') + '/'

    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'} # Extensiones que estan permitidas.
