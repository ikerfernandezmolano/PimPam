from flask import Blueprint, render_template

def home_blueprint():
    bp = Blueprint('home', __name__)

    @bp.route('/home')
    def index():
        return render_template('home.html')

    return bp
