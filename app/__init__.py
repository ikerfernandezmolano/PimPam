import os.path
import sqlite3

from flask import Flask

from app.controller.ui.equipos_controller import equipos_blueprint
from app.controller.ui.pokemon_controller import pokemon_blueprint

from app.controller.ui.pokedex_controller import pokedex_blueprint

from app.database.connection import Connection
from app.config import Config
from app.controller.ui.ControladorVista import *
from app.controller.ui.user_controlller import user_blueprint
from app.controller.ui.changelog_controller import changelog_blueprint
from app.database.connection import Connection

def init_db():
    print("Iniciando la base de datos")
    if os.path.exists(Config.DB_PATH):
        print("La base de datos existe")
        conn = sqlite3.connect(Config.DB_PATH)
        with open('app/database/schema.sql') as f:
            conn.executescript(f.read())
    conn = sqlite3.connect(Config.DB_PATH)
    try:
        with open('app/database/schema.sql') as f:
            print("Creando tablas con schema.sql...")
            conn.executescript(f.read())
    except Exception as e:
        print(f"Error creando tablas: {e}")
    finally:
        conn.close()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar base de datos
    init_db()

    # Crear conexión a la base de datos
    db = Connection()

    app.register_blueprint(equipos_blueprint(db))
    app.register_blueprint(pokemon_blueprint(db))
    app.register_blueprint(user_blueprint(db))
    app.register_blueprint(changelog_blueprint(db))
    app.register_blueprint(pokedex_blueprint(db))
    app.register_blueprint(home_blueprint())
    app.register_blueprint(signin_blueprint(db))
    app.register_blueprint(register_blueprint(db))

    return app
