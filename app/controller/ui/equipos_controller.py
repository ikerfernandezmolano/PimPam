from flask import Blueprint, render_template, session, redirect, url_for, request
from app.controller.model.GestorEquipos import GestorEquipos


def equipos_blueprint(db):
    bp = Blueprint("equipos", __name__)
    gestor = GestorEquipos(db)

    @bp.route("/equipos")
    def cargar_equipos():
        idUsuario = session.get("user_id", 1)

        equipos_db = gestor.getEquiposUsuario(idUsuario)
        equipos = []

        for fila in equipos_db:
            equipo = dict(fila)
            equipo["pokemon"] = gestor.getPokemonEquipo(equipo["IDEquipo"])
            equipos.append(equipo)

        pokedex = gestor.getPokedex()

        return render_template(
            "equipos.html",
            equipos=equipos,
            pokedex=pokedex
        )

    @bp.route("/equipos/crear", methods=["POST"])
    def crear_equipo():
        idUsuario = session.get("user_id", 1)
        nombre = request.form["nombre"]
        gestor.crearEquipo(idUsuario, nombre)
        return redirect(url_for("equipos.cargar_equipos"))

    @bp.route("/equipos/eliminar/<int:idEquipo>", methods=["POST"])
    def eliminar_equipo(idEquipo):
        gestor.eliminarEquipo(idEquipo)
        return redirect(url_for("equipos.cargar_equipos"))

    @bp.route("/equipos/<int:idEquipo>/modificar_nombre", methods=["POST"])
    def modificar_nombre_equipo(idEquipo):
        nombre = request.form["nombre"]
        gestor.modificarNombreEquipo(idEquipo, nombre)
        return redirect(url_for("equipos.cargar_equipos"))

    @bp.route("/equipos/<int:idEquipo>/pokemon", methods=["POST"])
    def modificar_pokemon(idEquipo):
        slot = request.form["slot"]
        idPokemon = request.form.get("idPokemon")

        if not idPokemon:
            gestor.eliminarPokemon(idEquipo, slot)
        else:
            gestor.reemplazarPokemon(idEquipo, slot, idPokemon)

        return redirect(url_for("equipos.cargar_equipos"))

    return bp
