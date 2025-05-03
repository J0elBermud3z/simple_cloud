import os
import threading


import time

from flask import Blueprint, request, redirect, jsonify, render_template
from flask import current_app

from app.extensions.ext import socketio,emit

from werkzeug.utils import secure_filename

from app.utils.functions import debug_message

file_bp = Blueprint('api', __name__,url_prefix='/api') 


def secure_path(base_dir:str, user_input:str) -> bool:

    if user_input == '/':
        return True
    
    user_path = os.path.normpath(os.path.join(base_dir, user_input))
    if os.path.commonprefix([user_path, base_dir]) != base_dir:
        return False
    
    return True

def format_directory(directory:str) -> str:

    return (directory.replace('-','/')).replace('.','')

def get_filetype(file:str) -> str:

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
            return jsonify({'message':'Not file part'}),400
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({'message':'No selected file'}),400

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOADED_FILES'],filename))
            return jsonify({'message':'¡File uploaded successfully!'}),200
    
    return redirect('/')

@file_bp.route('/delete/<file_name>', methods=['GET','POST'])
def delete_file(file_name):

    if request.method == 'POST':
        try:
            file_name = secure_filename(file_name)
            os.remove(os.path.join(current_app.config['UPLOADED_FILES'],file_name))

        except FileNotFoundError:
            return jsonify({'message':'¡File not found!'}),400
                
        return jsonify({'message':'¡File deleted successfully!'}),200

    
    return redirect('/')
 
@file_bp.route('/', methods=['GET'])
@file_bp.route('/<path:url>', methods=['GET'])
def all_files(url='/'): 

    all_files_and_directories = {}
    base_path = current_app.config['UPLOADED_FILES'] 
    debug_message(f" /api/ : Arg path value '{url}'",current_app.config['DEBUG_MODE'])
    
    url = format_directory(url)
    if secure_path(base_path,url):
        try:
            final_path = base_path + url
            all_files_and_directories['path']  = (url if url == '/' else '/' + url)
            files = [f for f in os.listdir(final_path) if os.path.isfile(os.path.join(final_path, f))] 
            directories = [d for d in os.listdir(final_path) if os.path.isdir(os.path.join(final_path, d))]

        except FileNotFoundError:
            all_files_and_directories['error'] = 'FileNotFoundError'
            return jsonify(all_files_and_directories)
    
    all_files_and_directories['directories'] = [d for d in directories]
    all_files_and_directories['files'] = [f for f in files]

    return jsonify(all_files_and_directories)

def check_files_thread(app,sid):

    with app.app_context():
        base_path = current_app.config['UPLOADED_FILES']         
        aux_new_files = len(os.listdir(base_path))
        
        while True:
            time.sleep(2)
            new_files = len(os.listdir(base_path))
            if new_files > aux_new_files:
                aux_new_files = new_files
                emit("new_files",{'new files or directories'},to=sid)


@socketio.on('connect')
def event_new_files():

    sid = request.sid
    app = current_app._get_current_object()
    thread = threading.Thread(target=check_files_thread, args=(app, sid))
    thread.daemon = True
    thread.start()