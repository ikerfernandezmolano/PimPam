from flask import Blueprint, render_template

def register_blueprint():
    bp = Blueprint('register', __name__)

    @bp.route('/register')
    def index():
        return render_template('register.html')

    return bp

