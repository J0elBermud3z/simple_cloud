from flask import Blueprint, redirect, render_template, request, flash, url_for


home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')