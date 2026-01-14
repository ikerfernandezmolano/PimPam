import unittest
import os
import sqlite3
import sys
import time 

sys.path.insert(0, os.getcwd()) 

from app import create_app
from app.config import Config 

TEST_DB = 'test_pimpam.db'

class TestChangelog(unittest.TestCase):
    """
    Clase de pruebas unitarias para validar el módulo Changelog.
    Utiliza una base de datos temporal que se reinicia en cada test.
    """

    def setUp(self):
        """CONFIGURACIÓN INICIAL: Se ejecuta ANTES de cada prueba."""
        # Limpieza de BD anterior si existe
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except PermissionError:
                time.sleep(0.1)
                try:
                    os.remove(TEST_DB)
                except:
                    pass 

        # Configuración de Flask para modo Testing
        Config.DB_PATH = TEST_DB
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        # Inicialización de datos semilla
        self._init_test_db()

    def tearDown(self):
        """LIMPIEZA: Se ejecuta DESPUÉS de cada prueba para borrar la BD."""
        if os.path.exists(TEST_DB):
            try:
                time.sleep(0.1)
                os.remove(TEST_DB)
            except PermissionError:
                pass 

    def _init_test_db(self):
        """Helper para crear tablas e insertar datos de prueba."""
        conn = sqlite3.connect(TEST_DB)
        cursor = conn.cursor()
        
        schema_path = os.path.join(os.getcwd(), 'app', 'database', 'schema.sql')
        with open(schema_path, 'r') as f:
            try:
                cursor.executescript(f.read())
            except sqlite3.OperationalError:
                pass 

        # Insertamos un usuario y un mensaje de prueba (Fixture)
        cursor.execute("INSERT OR IGNORE INTO Especie (PokedexID, Nombre, Generacion) VALUES (1, 'Bulbasaur', 1)")
        cursor.execute("INSERT OR IGNORE INTO Usuario (Nombre, Email, Contrasena, Estado, IDFavorito) VALUES (?, ?, ?, ?, ?)",
                       ('TestUser', 'test@test.com', '1234', 'Activo', 1))
        
        cursor.execute("""
            INSERT INTO Mensaje (IDUsuario, Texto, Fecha) 
            VALUES 
            ((SELECT IDUsuario FROM Usuario WHERE Nombre='TestUser'), 'Capturó un Pikachu', '12/01/2025')
        """)
        
        conn.commit()
        conn.close()

    # --- CASOS DE PRUEBA ---

    def test_2A_listado_basico(self):
        """Verifica que la página carga y muestra los datos iniciales."""
        response = self.client.get('/changelog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pikachu', response.data)

    def test_2B_feed_vacio(self):
        """Verifica el mensaje de 'No hay actividad' cuando la BD está vacía."""
        conn = sqlite3.connect(TEST_DB)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Mensaje") # Borramos datos
        conn.commit()
        conn.close()

        response = self.client.get('/changelog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No hay actividad reciente', response.data)

    def test_2C_boton_volver(self):
        """Verifica que existe el elemento de navegación para volver atrás."""
        response = self.client.get('/changelog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'return.png', response.data)

    def test_4D_buscar_usuario_existente(self):
        """Verifica el filtro de búsqueda con un usuario que SÍ existe."""
        response = self.client.post('/changelog', data={'busqueda': 'TestUser'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pikachu', response.data)

    def test_4D_buscar_usuario_inexistente(self):
        """Verifica el filtro de búsqueda con un usuario que NO existe."""
        response = self.client.post('/changelog', data={'busqueda': 'Gaspar'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Pikachu', response.data)

    def test_4A_boton_todos(self):
        """Verifica que se puede resetear el filtro volviendo a cargar la vista general."""
        self.client.post('/changelog', data={'busqueda': 'Gaspar'})
        response = self.client.get('/changelog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pikachu', response.data)

if __name__ == '__main__':
    unittest.main()