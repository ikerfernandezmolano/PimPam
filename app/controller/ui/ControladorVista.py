from flask import Blueprint, request, redirect, render_template, flash, url_for
from app.controller.model.GestorUsuarios import GestorUsuarios
from flask import get_flashed_messages

def home_blueprint():
    bp = Blueprint('home', __name__)

    @bp.route('/')
    def root():
        return redirect(url_for('home.index'))

    @bp.route('/home')
    def index():
        return render_template('home.html')

    return bp
    
def db_blueprint(db):
    bp = Blueprint('db', __name__)
    service = GestorUsuarios(db)

    @bp.route('/db')
    def db():
        users = service.get_all()
        from app.controller.model.Sesion import Sesion
        sesion = Sesion()
        usuario_sesion = sesion.usuario  # puede ser None si nadie ha iniciado sesión
        return render_template('db.html', usuarios=users, usuario_sesion=usuario_sesion)

    return bp

def register_blueprint(db):
    bp = Blueprint('register', __name__)
    service = GestorUsuarios(db)

    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            user = request.form.get('user')
            email = request.form.get('email')
            password = request.form.get('password', '').strip()
            password_confirm = request.form.get('confirm_password', '').strip()

            if password != password_confirm:
                flash("Las contraseñas no coinciden", "error")
            else:
                try:
                    service.añadirUsuario(user, email, password)
                    flash("Usuario creado correctamente", "success")
                    return redirect(url_for('register.register'))
                except ValueError as e:
                    flash(str(e), "error")
        mensajes = get_flashed_messages(with_categories=True)
        return render_template('register.html', mensajes=mensajes)

    return bp

def signin_blueprint(db):
    bp = Blueprint('signin', __name__)
    service = GestorUsuarios(db)

    @bp.route('/signin', methods=['GET', 'POST'])
    def signin():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password', '').strip()
            status = service.iniciarSesion(email,password)
            if status == 0:
                return redirect(url_for('pokedex.index'))
            elif status == 1:
                flash("EL USUARIO NO EXISTE", "error")
            elif status == 2:
                flash("CONTRASEÑA INCORRECTA", "error")
            elif status == 3:
                flash("USUARIO AÚN NO ACEPTADO", "error")
            else:
                flash("ERROR DESCONOCIDO, INTÉNTALO MÁS TARDE", "error")

        mensajes = get_flashed_messages(with_categories=True)
        return render_template('signin.html', mensajes=mensajes)

    return bp

