from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import current_app


file_bp = Blueprint('file', __name__,url_prefix='/file') 

@file_bp.route('/upload')
def upload_file():

    UPLOADED_FILES_PATH = current_app.config['UPLOADED_FILES']
    return f'Testing {UPLOADED_FILES_PATH}'