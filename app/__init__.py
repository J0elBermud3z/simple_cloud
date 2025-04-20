from flask import Flask
from .config import Paths
from .config import Config
from .controllers.files_controller import file_bp
from .controllers.home_controller import home_bp

import os

def create_app():
    
    app = Flask(__name__, template_folder='views')
    app.config.from_object(Paths)
    app.config.from_object(Config)

    app.register_blueprint(file_bp)
    app.register_blueprint(home_bp)

    return app