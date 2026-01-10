from flask import Blueprint, render_template

def signin_blueprint():
    bp = Blueprint('signin', __name__)

    @bp.route('/signin')
    def index():
        return render_template('signin.html')

    return bp

