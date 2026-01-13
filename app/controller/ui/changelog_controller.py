from flask import Blueprint, render_template, request
from app.controller.model.changelog_controller import ChangelogController

def changelog_blueprint(db):
    bp = Blueprint("changelog", __name__)
    
    model = ChangelogController(db) 

    @bp.route("/changelog", methods=["GET", "POST"])
    def ver_changelog():
        mensajes = []
        busqueda = "" 

        if request.method == "POST":
            # Si alguien busca, filtramos por nombre
            busqueda = request.form.get("busqueda", "")
            mensajes = model.filtrar_mensajes_por_usuario(busqueda)
        else:
            # Si entran normal, mostramos todo el historial
            mensajes = model.obtener_todos_mensajes()

        return render_template("changelog.html", mensajes=mensajes)

    return bp