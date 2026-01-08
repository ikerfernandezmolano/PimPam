import os.path
import sqlite3

from flask import Flask

from app.controller.ui.equipos_controller import equipos_blueprint
from app.controller.ui.pokemon_controller import pokemon_blueprint

from app.database.connection import Connection
from app.config import Config


def init_db():
    print("Iniciando la base de datos")
    if os.path.exists(Config.DB_PATH):
        print("La base de datos existe")
        conn = sqlite3.connect(Config.DB_PATH)
        with open('app/database/schema.sql') as f:
            conn.executescript(f.read())
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

    return app