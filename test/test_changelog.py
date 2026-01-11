import unittest
import os
import sqlite3
import sys
import time # Necesario para esperar a Windows

# --- FUERZA BRUTA: RUTA ABSOLUTA ---
sys.path.insert(0, os.getcwd()) 
# -----------------------------------

from app import create_app
from app.config import Config 

TEST_DB = 'test_pimpam.db'

class TestChangelog(unittest.TestCase):

    def setUp(self):
        """Se ejecuta ANTES de cada prueba"""
        # 1. LIMPIEZA PREVENTIVA: Intentamos borrar la DB por si se quedó de antes
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except PermissionError:
                # Si Windows no la suelta, esperamos un poquito y reintentamos
                time.sleep(0.1)
                try:
                    os.remove(TEST_DB)
                except:
                    pass # Si no se puede, seguimos (confiamos en INSERT OR IGNORE)

        # 2. Configuración normal
        Config.DB_PATH = TEST_DB
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        # 3. Inicializar datos
        self._init_test_db()

    def tearDown(self):
        """Se ejecuta DESPUÉS de cada prueba"""
        # Cerramos conexiones explícitamente para liberar el archivo
        if os.path.exists(TEST_DB):
            try:
                # Esperamos un momento para que el sistema suelte el archivo
                time.sleep(0.1)
                os.remove(TEST_DB)
            except PermissionError:
                pass # No pasa nada, lo borrará el siguiente setUp

    def _init_test_db(self):
        conn = sqlite3.connect(TEST_DB)
        cursor = conn.cursor()
        
        # Leemos el esquema
        schema_path = os.path.join(os.getcwd(), 'app', 'database', 'schema.sql')
        with open(schema_path, 'r') as f:
            # Usamos un try/except aquí porque a veces create_app ya crea las tablas
            try:
                cursor.executescript(f.read())
            except sqlite3.OperationalError:
                pass # Si las tablas ya existen, no pasa nada

        # --- AQUÍ ESTÁ LA MAGIA: INSERT OR IGNORE ---
        # Si el usuario ya existe (porque no se pudo borrar la DB), no da error.
        
        # 1. Insertar Especie (Bulbasaur)
        cursor.execute("INSERT OR IGNORE INTO Especie (PokedexID, Nombre, Generacion) VALUES (1, 'Bulbasaur', 1)")

        # 2. Insertar Usuario (TestUser)
        # Usamos OR IGNORE para evitar el error "UNIQUE constraint failed"
        cursor.execute("INSERT OR IGNORE INTO Usuario (Nombre, Email, Contrasena, Estado, IDFavorito) VALUES (?, ?, ?, ?, ?)",
                       ('TestUser', 'test@test.com', '1234', 'Activo', 1))
        
        # 3. Insertar Mensaje
        # Primero borramos mensajes anteriores de este usuario para no duplicar en el test
        cursor.execute("DELETE FROM Mensaje WHERE IDUsuario = (SELECT IDUsuario FROM Usuario WHERE Nombre='TestUser')")
        
        cursor.execute("""
            INSERT INTO Mensaje (IDUsuario, Texto, Fecha) 
            VALUES 
            ((SELECT IDUsuario FROM Usuario WHERE Nombre='TestUser'), 'Capturó un Pikachu', '12/01/2025')
        """)
        
        conn.commit()
        conn.close()

    # --- PRUEBAS ---
    def test_2A_listado_basico(self):
        response = self.client.get('/changelog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pikachu', response.data)

    def test_4D_buscar_usuario_existente(self):
        response = self.client.post('/changelog', data={'busqueda': 'TestUser'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pikachu', response.data)

    def test_4D_buscar_usuario_inexistente(self):
        response = self.client.post('/changelog', data={'busqueda': 'Gaspar'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Pikachu', response.data)

if __name__ == '__main__':
    unittest.main()