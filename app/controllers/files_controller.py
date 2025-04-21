import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app

file_bp = Blueprint('api', __name__) 

def get_filetype(file:str):
    file_extension = file.split('.')[1]
    
    if len(file) >= 7:
        file = file[0:4] + '...'

    if file_extension in current_app.config['IMAGE_EXTENSIONS']:
        return ('image.svg',file)
    
    if file_extension in current_app.config['TEXT_EXTENSIONS']:
        return ('file-text.svg',file)
    
    

@file_bp.route('/upload', methods=['GET','POST'])
def upload_file():

    if request.method == 'POST':
        if 'file' not in request.files:
            # flash('Not file part') 
            return redirect('/')
        
        file = request.files['file']

        if file.filename == '':
            # flash('No selected file')
            return redirect('/')

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOADED_FILES'],filename))
            return '¡File uploaded successfully!'
    
    return redirect('/')

@file_bp.route('/delete/<file_name>', methods=['GET','POST'])
def delete_file(file_name):

    if request.method == 'POST':
        try:
            file_name = secure_filename(file_name)
            os.remove(os.path.join(current_app.config['UPLOADED_FILES'],file_name))
        except FileNotFoundError:
            return '¡File not found!'        
                
        return '¡File deleted successfully!'
    
    return redirect('/')
 
@file_bp.route('/', methods=['GET'])
def all_files():

    all_files = {}
    files = os.listdir(current_app.config['UPLOADED_FILES'])
    files.sort()

    page = request.args.get('page', 1, type=int) # Obtengo la pagina (?page=1)
    per_page = 20 # Limito la cantidad de resultados
    total = len(files) 
    start = (page - 1) * per_page # Obtengo 
    end = start + per_page

    files_paginated = files[start:end]

    for file in files_paginated:
        all_files[file] = get_filetype(file)
    
    return render_template('index.html',all_files=all_files, page=page, total=total, per_page=per_page)

