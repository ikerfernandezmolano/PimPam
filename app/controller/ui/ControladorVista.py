from flask import Blueprint, render_template, redirect, url_for
from app.controller.model.GestorUsuarios import GestorUsuarios

def home_blueprint():
    bp = Blueprint('home', __name__)

    @bp.route('/')
    def root():
        return redirect(url_for('home.index'))

    @bp.route('/home')
    def index():
        return render_template('home.html')

    return bp

def register_blueprint(db):
    bp = Blueprint('register', __name__)
    service = GestorUsuarios(db)

    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        return render_template('register.html')

    return bp

def signin_blueprint(db):
    bp = Blueprint('signin', __name__)
    service = GestorUsuarios(db)

    @bp.route('/signin')
    def index():
        return render_template('signin.html')

    return bp

