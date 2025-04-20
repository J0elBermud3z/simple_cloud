import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app

file_bp = Blueprint('file', __name__,url_prefix='/file') 

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

