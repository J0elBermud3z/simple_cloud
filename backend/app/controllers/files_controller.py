import os
import shutil
import threading
import time
from flask import Blueprint, request, redirect, jsonify
from flask import current_app
from app.extensions.ext import socketio,emit
from werkzeug.utils import secure_filename
from app.utils.functions import debug_message
from app.utils.filesystem import format_directory,secure_path,have_files,get_path_size,get_total_files_and_directories, get_filetype,delete_first_bar, format_root

file_bp = Blueprint('api', __name__, url_prefix='/api/') 

@file_bp.route('/file/', methods=['POST'])
@file_bp.route('/file/<path:folder_path>', methods=['POST'])
def upload_file(folder_path='') -> dict: # Json dict, redirect
    base_path = current_app.config['UPLOADED_FILES']
    final_path = os.path.join(base_path,folder_path)

    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            save_path = (os.path.join(final_path, filename) if folder_path != '/' else base_path)
            file.save(save_path)
            return jsonify({
            'status': 'success',
            'data': {
                'name': filename,
                'type': 'file',
                'size': get_path_size(final_path),
                'path': format_root(folder_path)
            }
        }), 200

    else:
        return jsonify({'status':'error','message': 'No file selected'}), 400

@file_bp.route('/folder/<path:folder_path>', methods=['POST'])
def create_directory(folder_path=''):
    
    base_path = current_app.config['UPLOADED_FILES']
    final_path = os.path.join(base_path,folder_path)
    
    if not os.path.exists(final_path):
        folder_name = folder_path.split('/')[-1]
        os.makedirs(final_path)
        return jsonify({
        'status': 'success',
        'data': {
            'name': folder_name,
            'type': 'directory',
            'size': get_path_size(final_path),
            'path': format_root(folder_path)
        }
    }), 200

    else:
        return jsonify({'status':'error',
                        'message': 'Directory already exists'
                        }), 409


@file_bp.route('/<old_name>/<new_name>', methods=['PATCH'])
@file_bp.route('/<path:folder_path>/<old_name>/<new_name>', methods=['PATCH'])
def rename_file(old_name, new_name, folder_path=''):

    base_path = current_app.config['UPLOADED_FILES']

    old_path = os.path.join(base_path, folder_path, old_name)
    new_path = os.path.join(base_path, folder_path, new_name)

    if os.path.exists(old_path):
        try:
            os.rename(old_path, new_path)
            return jsonify({'status':'success',
                            'message': f'¡{"Directory" if os.path.isdir(new_path) else "File"} renamed successfully!'
                            }), 200
        
        except Exception as e:
            return jsonify({'status':'error',
                            'message': f'Error renaming file or directory: {str(e)}'
                            }), 500
    
    return jsonify({'status':'error',
                    'message': '¡File or directory not found!'
                    }), 404


@file_bp.route('/<path:file_name>', methods=['DELETE'])
def delete_file(file_name) -> dict: # Json dict, redirect

    file_path = os.path.join(current_app.config['UPLOADED_FILES'],file_name) 

    if os.path.exists(file_path):
        file_name = secure_filename(file_name)
        if os.path.isfile(file_path):
            os.remove(os.path.join(current_app.config['UPLOADED_FILES'],file_name))
            return jsonify({'status':'success',
                            'message':'¡File deleted successfully!'
                            }),200

        else:
            shutil.rmtree(file_path, ignore_errors=True)
            return jsonify({'status':'success',
                            'message':'¡Directory deleted successfully!'
                            }),200           
    
    return jsonify({'status':'error',
                    'message':f'¡File or directory not found!'
                    }),404
 
@file_bp.route('/', methods=['GET'])
@file_bp.route('/<path:url>', methods=['GET'])
def all_files(url='/') -> dict: # Json dict  

    all_files_and_directories = {}
    base_path = current_app.config['UPLOADED_FILES'] 
    debug_message(f" /api/ : Arg path value '{url}'",current_app.config['DEBUG_MODE'])
    print('ruta',base_path,' ',url)

    url = format_directory(url)
    if secure_path(base_path,url):
        try:
            final_path = os.path.join(base_path, url.strip('/'))
            all_files_and_directories['path']        = (url if url == '/' else '/'+url)
            all_files_and_directories['files']       = [{'name':f,'type':get_filetype(final_path + '/' + f)} for f in os.listdir(final_path) if os.path.isfile(os.path.join(final_path, f))] 
            all_files_and_directories['directories'] = sorted([{'isEmpty': have_files(final_path + '/' + d), 'name':d} for d in os.listdir(final_path) if os.path.isdir(os.path.join(final_path, d))], key= lambda x: x['isEmpty'])
            all_files_and_directories['actions']     = [{'label':'Create Directory', 'method':'POST', 'url':'/api/'+url+'/new_directory/' if url != '/' else '/api/new_directory/'},
                                                       {'label':'Upload File', 'method':'POST', 'url':'/api/file/'+url if url != '/' else '/api/file/'}]
            
            if url != '/': # Operations are not allowed in the root path '/'.
                all_files_and_directories['actions'].append({'label':'Delete', 'method':'DELETE', 'url':'/api/'+url})
                all_files_and_directories['actions'].append({'label':'Rename', 'method':'PATCH', 'url':'/api/'+url+'/old_name/new_name'})
                all_files_and_directories['actions'].append({'label':'Get path size', 'method':'GET','url':'/api/size?path='+url}) 


        except FileNotFoundError:

            return jsonify({'status':'error',
                            'message': 'File or Directory Not Found'
                            }), 404

    else:
        return jsonify({'status':'error',
                        'message': 'Path not allowed'
                        }), 404
    
    return jsonify({'status':'success'
                    ,'data':all_files_and_directories
                    }),200


@file_bp.route('/size', methods=['GET'])
def get_file_size():

    base_path = current_app.config['UPLOADED_FILES'] 
        
    path_parameter = request.args.get('path')
    if not path_parameter:
        return jsonify({'message':f'¡Missing parameter path!'}),404

    path_parameter =  (delete_first_bar(path_parameter) if path_parameter.startswith('/') else path_parameter)
    file_path = os.path.join(base_path, path_parameter)

    if not secure_path(base_path, path_parameter) or not os.path.exists(file_path):
        return jsonify({'message':f'¡File or directory not found!'}),404

    return jsonify({'status':'success',
                    'data':{'path':'/' + path_parameter.strip('/'),
                    'name': os.path.basename(file_path),
                    'size':get_path_size(file_path)}
                    }),200

    
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