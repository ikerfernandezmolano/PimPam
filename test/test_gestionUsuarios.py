import unittest
import os
import sqlite3
import sys
import time

# Añade el directorio raíz al path para poder importar la app
sys.path.insert(0, os.getcwd())

from app import create_app
from app.config import Config

# Base de datos de pruebas
TEST_DB = 'test_pimpam.db'


class TestUsuarios(unittest.TestCase):

    def setUp(self):
        # Elimina la base de datos de test si existe
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except PermissionError:
                time.sleep(0.1)

        # Configura la ruta de la BD de pruebas
        Config.DB_PATH = TEST_DB
        self._init_test_db()

        # Crea la aplicación en modo testing
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        # Limpia cliente y app tras cada test
        self.client = None
        self.app = None

        # Elimina la base de datos de pruebas
        if os.path.exists(TEST_DB):
            try:
                time.sleep(0.1)
                os.remove(TEST_DB)
            except PermissionError:
                pass

    def _init_test_db(self):
        # Inicializa la base de datos con el esquema y datos mínimos
        conn = sqlite3.connect(TEST_DB, timeout=10)
        cursor = conn.cursor()

        schema_path = os.path.join(os.getcwd(), 'app', 'database', 'schema.sql')
        with open(schema_path, 'r') as f:
            try:
                cursor.executescript(f.read())
            except sqlite3.OperationalError:
                pass
                
        # DATOS SEMILLA BÁSICOS
        cursor.execute("INSERT OR IGNORE INTO Especie (PokedexID, Nombre, Generacion) VALUES (1, 'Bulbasaur', 1)")
        cursor.execute("INSERT OR IGNORE INTO Especie (PokedexID, Nombre, Generacion) VALUES (4, 'Charmander', 1)")

        # Usuario 1 (Admin)
        cursor.execute("INSERT OR IGNORE INTO Usuario (IDUsuario, Nombre, Email, Estado, IDFavorito) VALUES (1, 'Admin', 'admin@test.com', 'Aceptado', 1)")
        # Usuario 2 (Normal)
        cursor.execute("INSERT OR IGNORE INTO Usuario (IDUsuario, Nombre, Email, Estado, IDFavorito) VALUES (2, 'UsuarioNormal', 'user@test.com', 'Aceptado', 4)")

        conn.commit()
        conn.close()

    # --- PRUEBAS ---

    def test_1_inicarSesion(self):
        # Comprueba que se puede acceder a la vista de equipos
        response = self.client.get('/inicioSesion')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EquipoDemo', response.data)

if __name__ == '__main__':
    unittest.main()
