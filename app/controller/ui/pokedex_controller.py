from flask import Blueprint, render_template

def pokedex_blueprint(db):
    bp = Blueprint('pokedex', __name__)

    @bp.route('/pokedex')
    def index():
        # Datos para el panel IZQUIERDO (el destacado)
        pokemon_destacado = {
            "id": 658,
            "nombre": "GRENINJA",
            "tipo1": "AGUA",
            "tipo2": "SINIESTRO",
            "descripcion": "PUEDE DETECTAR ENEMIGOS FUERA DE SU CAMPO VISUAL AL CAPTAR LOS MOVIMIENTOS DEL AIRE CON SU LARGA LENGUA ENROSCADA ALREDEDOR DEL CUELLO.",
            "altura": "1,50 M",
            "peso": "40 KG",
            "categoria": "NINJA",
            "imagen": "greninja.png"
        }

        # Datos para la lista de la DERECHA
        lista_pokemon = [
            {"id": 133, "nombre": "EEVEE", "tipo1": "NORMAL", "tipo2": None, "imagen": "eevee.png"},
            {"id": 94, "nombre": "GENGAR", "tipo1": "FANTASMA", "tipo2": "VENENO", "imagen": "gengar.png"},
            {"id": 59, "nombre": "ARCANINE", "tipo1": "FUEGO", "tipo2": None, "imagen": "arcanine.png"},
            {"id": 470, "nombre": "LEAFEON", "tipo1": "PLANTA", "tipo2": None, "imagen": "leafeon.png"},
            {"id": 6, "nombre": "CHARIZARD", "tipo1": "FUEGO", "tipo2": "VOLADOR", "imagen": "charizard.png"},
            {"id": 25, "nombre": "PIKACHU", "tipo1": "ELÉCTRICO", "tipo2": None, "imagen": "pikachu.png"},
        ]

        return render_template('pokedex.html', destacado=pokemon_destacado, pokemons=lista_pokemon)

    return bp