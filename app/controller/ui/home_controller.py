from flask import Blueprint, render_template, redirect, url_for

def home_blueprint():
    bp = Blueprint('home', __name__)

    @bp.route('/')
    def root():
        return redirect(url_for('home.index'))

    @bp.route('/home')
    def index():
        return render_template('home.html')

    return bp

