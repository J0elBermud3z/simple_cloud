import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app

file_bp = Blueprint('file', __name__,url_prefix='/file') 

def allowed_file(filename):

    ext = os.path.splitext(filename)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


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

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOADED_FILES'],filename))
            return 'File uploaded successfully'
    
    return redirect('/')

