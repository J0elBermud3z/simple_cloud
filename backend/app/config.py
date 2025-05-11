import os 

class Config:


    DEBUG_MODE = True

class Paths:

    MAIN_PATH = str(os.path.abspath(__file__)).replace('/config.py','/')
    UPLOADED_FILES = os.path.join(MAIN_PATH,'uploaded_files') + '/'

    IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'svg', 'ico', 'heic', 'avif']
    TEXT_EXTENSIONS = ['txt', 'md', 'csv', 'log', 'json', 'xml', 'yaml', 'yml', 'ini']
    DOC_EXTENSIONS = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'ods', 'odp', 'rtf']
    CODE_EXTENSIONS = [
    'py',   # Python
    'js',   # JavaScript
    'ts',   # TypeScript
    'java', # Java
    'c', 'cpp', 'h', 'hpp',  # C/C++
    'cs',   # C#
    'rb',   # Ruby
    'php',  # PHP
    'go',   # Go
    'rs',   # Rust
    'sh',   # Shell
    'bat',  # Batch
    'ps1',  # PowerShell
    'html', 'htm',  # HTML
    'css',  # CSS
    'json', 'xml', 'yaml', 'yml',  # Configuración y datos
    'sql',  # SQL
    'kt',   # Kotlin
    'swift',# Swift
    'r',    # R
    'pl',   # Perl
    'scala',# Scala
    'lua',  # Lua
    'dart', # Dart
    'asm',  # Ensamblador
    'tsv',  # Tab-separated values, útil para datos también
    ]

