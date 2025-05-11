import os
import threading
import time
from flask import Blueprint, request, redirect, jsonify, render_template
from flask import current_app
from app.extensions.ext import socketio,emit
from werkzeug.utils import secure_filename
from app.utils.functions import debug_message
from app.utils.filesystem import format_directory,secure_path,have_files,get_total_files_and_directories

file_bp = Blueprint('api', __name__,url_prefix='/api') 


@file_bp.route('/upload', methods=['POST'])
def upload_file() -> dict: # Json dict or redirect

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

@file_bp.route('/delete/<file_name>', methods=['POST'])
def delete_file(file_name) -> dict: # Json dict, redirect

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
def all_files(url='/') -> dict: # Json dict  

    all_files_and_directories = {}
    base_path = current_app.config['UPLOADED_FILES'] 
    debug_message(f" /api/ : Arg path value '{url}'",current_app.config['DEBUG_MODE'])
    
    url = format_directory(url)
    if secure_path(base_path,url):
        try:
            final_path = os.path.join(base_path, url.strip('/'))
            all_files_and_directories['path']  = (url if url == '/' else '/' + url)
            files = [f for f in os.listdir(final_path) if os.path.isfile(os.path.join(final_path, f))] 
            directories = [d for d in os.listdir(final_path) if os.path.isdir(os.path.join(final_path, d))]

        except FileNotFoundError:
            all_files_and_directories['error'] = 'FileNotFoundError'
            return jsonify(all_files_and_directories)
    else:
        return jsonify({'error': 'Path not allowed'}), 400
    
    all_files_and_directories['directories'] = sorted([{d: have_files(final_path+'/'+d)} for d in directories], key=lambda x: not next(iter(x.values()))) 
    all_files_and_directories['files'] = [f for f in files]

    return jsonify(all_files_and_directories)

def check_files_thread(app,sid):

    with app.app_context():
        base_path = current_app.config['UPLOADED_FILES']         
        aux_new_files = get_total_files_and_directories(base_path)
        
        while True:
            time.sleep(1)
            new_files = get_total_files_and_directories(base_path)
            if new_files != aux_new_files:
                aux_new_files = new_files
                socketio.emit('new_files', {'message': 'Nuevo archivo'}, to=sid)


@socketio.on('connect')
def on_connect():

    sid = request.sid
    app = current_app._get_current_object()
    thread = threading.Thread(target=check_files_thread, args=(app, sid))
    thread.daemon = True
    thread.start()