import unittest
import os
import sqlite3
import sys
import time

sys.path.insert(0, os.getcwd())

from app import create_app
from app.config import Config

TEST_DB = 'test_pimpam.db'


class TestEquipos(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except PermissionError:
                time.sleep(0.1)
                try:
                    os.remove(TEST_DB)
                except:
                    pass

        Config.DB_PATH = TEST_DB
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        self._init_test_db()

    def tearDown(self):
        if os.path.exists(TEST_DB):
            try:
                time.sleep(0.1)
                os.remove(TEST_DB)
            except PermissionError:
                pass

    def _init_test_db(self):
        conn = sqlite3.connect(TEST_DB)
        cursor = conn.cursor()

        schema_path = os.path.join(os.getcwd(), 'app', 'database', 'schema.sql')
        with open(schema_path, 'r') as f:
            try:
                cursor.executescript(f.read())
            except sqlite3.OperationalError:
                pass

        cursor.execute(
            "INSERT OR IGNORE INTO Usuario (Nombre, Email, Contrasena, Estado) VALUES (?, ?, ?, ?)",
            ('TestUser', 'test@test.com', '1234', 'Activo')
        )

        cursor.execute(
            "INSERT OR IGNORE INTO Especie (PokedexID, Nombre, Generacion) VALUES (25, 'Pikachu', 1)"
        )

        cursor.execute("""
            INSERT OR IGNORE INTO Equipo (Nombre, IDUsuario)
            VALUES ('Equipo Test', (SELECT IDUsuario FROM Usuario WHERE Nombre='TestUser'))
        """)

        conn.commit()
        conn.close()

    # --- PRUEBAS ---

    def test_2_acceso_gestion_equipos(self):
        response = self.client.get('/equipos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Equipo Test', response.data)

    def test_3_crear_equipo(self):
        response = self.client.post('/equipos/crear', data={'nombre': 'Equipo Nuevo'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/equipos')
        self.assertIn(b'Equipo Nuevo', response.data)

    def test_4_seleccionar_equipo(self):
        response = self.client.get('/equipos')
        self.assertEqual(response.status_code, 200)

    def test_5_anadir_pokemon(self):
        response = self.client.post(
            '/equipos/1/pokemon',
            data={'slot': 0, 'idPokemon': 25}
        )
        self.assertEqual(response.status_code, 302)

    def test_6_eliminar_pokemon(self):
        response = self.client.post(
            '/equipos/1/pokemon',
            data={'slot': 0, 'idPokemon': '__empty__'}
        )
        self.assertEqual(response.status_code, 302)

    def test_7_modificar_nombre_equipo(self):
        response = self.client.post(
            '/equipos/1/modificar_nombre',
            data={'nombre': 'Equipo Modificado'}
        )
        self.assertEqual(response.status_code, 302)

    def test_8_eliminar_equipo(self):
        response = self.client.post('/equipos/eliminar/1')
        self.assertEqual(response.status_code, 302)

    def test_10_volver_pokedex(self):
        response = self.client.get('/pokedex')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
