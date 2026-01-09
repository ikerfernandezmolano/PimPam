from flask import Blueprint, render_template, request
# Importamos la clase del MODELO usando la ruta completa para evitar confusión
from app.controller.model.changelog_controller import ChangelogController

def changelog_blueprint(db):
    bp = Blueprint("changelog", __name__)
    model = ChangelogController(db) # Instanciamos el modelo

    @bp.route("/changelog", methods=["GET", "POST"])
    def ver_changelog():
        mensajes = []
        
        if request.method == "POST":
            busqueda = request.form.get("busqueda", "")
            mensajes = model.filtrar_mensajes_por_usuario(busqueda)
        else:
            mensajes = model.obtener_todos_mensajes()

        return render_template("changelog.html", mensajes=mensajes)

    return bp 