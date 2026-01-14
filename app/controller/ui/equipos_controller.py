from flask import Blueprint, render_template, session, redirect, url_for, request
from app.controller.model.GestorEquipos import GestorEquipos


def equipos_blueprint(db):
    # Se crea el blueprint de equipos y el gestor asociado
    bp = Blueprint("equipos", __name__)
    gestor = GestorEquipos(db)

    @bp.route("/equipos")
    def cargar_equipos():
        # Obtiene el usuario de la sesión (por defecto 1)
        idUsuario = session.get("user_id", 1)

        # Equipo que se quiere mostrar como activo
        equipo_activo_id = request.args.get("equipo_id", type=int)

        # Carga los equipos del usuario
        equipos_db = gestor.getEquiposUsuario(idUsuario)
        equipos = []

        # Para cada equipo se cargan sus Pokémon
        for fila in equipos_db:
            equipo = dict(fila)
            equipo["pokemon"] = gestor.getPokemonEquipo(equipo["IDEquipo"])
            equipos.append(equipo)

        # Si el usuario no tiene equipos, se muestra la vista vacía
        if not equipos:
            return render_template(
                "equipos.html",
                equipos=[],
                equipo_activo=None,
                pokedex=[]
            )

        # Selección del equipo activo
        if equipo_activo_id:
            equipo_activo = next(
                (e for e in equipos if e["IDEquipo"] == equipo_activo_id),
                equipos[0]
            )
        else:
            equipo_activo = equipos[0]

        # Se obtienen los Pokémon disponibles para el desplegable
        pokedex = gestor.getPokedex()

        return render_template(
            "equipos.html",
            equipos=equipos,
            equipo_activo=equipo_activo,
            pokedex=pokedex
        )

    @bp.route("/equipos/crear", methods=["POST"])
    def create_equipo():
        # Crea un nuevo equipo para el usuario
        idUsuario = session.get("user_id", 1)
        nombre = request.form["nombre"]
        idEquipo = gestor.saveNewEquipo(idUsuario, nombre)

        # Redirige mostrando el nuevo equipo como activo
        return redirect(url_for("equipos.cargar_equipos", equipo_id=idEquipo))

    @bp.route("/equipos/eliminar/<int:idEquipo>", methods=["POST"])
    def deleteEquipo(idEquipo):
        # Elimina un equipo completo
        gestor.deleteEquipo(idEquipo)
        return redirect(url_for("equipos.cargar_equipos"))

    @bp.route("/equipos/<int:idEquipo>/modificar_nombre", methods=["POST"])
    def modifyName(idEquipo):
        # Modifica el nombre de un equipo
        nombre = request.form["nombre"]
        gestor.saveNewNombre(idEquipo, nombre)
        return redirect(url_for("equipos.cargar_equipos", equipo_id=idEquipo))

    @bp.route("/equipos/<int:idEquipo>/pokemon", methods=["POST"])
    def OpcionesModificarPokemon(idEquipo):
        # Gestiona las opciones de un slot del equipo
        slot = int(request.form["slot"])
        idPokemon = request.form.get("idPokemon")

        # Si se selecciona vacío, se elimina el Pokémon del slot
        if idPokemon == "__empty__":
            gestor.deleteEquipo(idEquipo, slot)
        else:
            # Si se selecciona un Pokémon, se reemplaza en el slot
            gestor.reemplazarPokemon(idEquipo, slot, int(idPokemon))

        return redirect(url_for("equipos.cargar_equipos", equipo_id=idEquipo))

    return bp
