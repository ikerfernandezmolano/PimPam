from flask import Blueprint, render_template, request
from app.controller.model.changelog_controller import ChangelogController

def changelog_blueprint(db):
    # Creamos el Blueprint para modularizar la sección del Changelog
    bp = Blueprint("changelog", __name__)
    
    # Instanciamos el controlador del modelo pasándole la conexión a la BD
    model = ChangelogController(db) 

    @bp.route("/changelog", methods=["GET", "POST"])
    def ver_changelog():
        """
        Ruta principal del Changelog.
        - GET: Muestra todos los mensajes (carga inicial o botón 'Todos').
        - POST: Procesa el formulario de búsqueda para filtrar mensajes.
        """
        mensajes = []
        busqueda = "" 

        # Verificamos si el usuario ha enviado el formulario de búsqueda
        if request.method == "POST":
            # Obtenemos el término de búsqueda del input del HTML
            busqueda = request.form.get("busqueda", "")
            # Llamamos al modelo para filtrar
            mensajes = model.filtrar_mensajes_por_usuario(busqueda)
        else:
            # Si es una petición GET (acceso normal), traemos todo el historial
            mensajes = model.obtener_todos_mensajes()

        # Renderizamos la plantilla HTML pasando la lista de mensajes procesada
        return render_template("changelog.html", mensajes=mensajes)

    return bp