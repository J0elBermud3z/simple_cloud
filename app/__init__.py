from flask import Flask, redirect
from .config import Paths
from .config import Config
from .controllers.files_controller import file_bp
from .controllers.home_controller import home_bp
from .controllers.error_handlers import register_error_handlers
from .extensions.ext import socketio

import os

    

def create_app():
    
    app = Flask(__name__, template_folder='views')
    
    app.config.from_object(Paths)
    app.config.from_object(Config)

    app.register_blueprint(file_bp)
    app.register_blueprint(home_bp)
    
    socketio.init_app(app)

    #register_error_handlers(app)
    return app