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

    def setUp(self):
        """Se ejecuta ANTES de cada prueba"""
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
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        self._init_test_db()

    def tearDown(self):
        """Se ejecuta DESPUÉS de cada prueba"""
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

        # Insertamos datos de prueba
        cursor.execute("INSERT OR IGNORE INTO Especie (PokedexID, Nombre, Generacion) VALUES (1, 'Bulbasaur', 1)")
        cursor.execute("INSERT OR IGNORE INTO Usuario (Nombre, Email, Contrasena, Estado, IDFavorito) VALUES (?, ?, ?, ?, ?)",
                       ('TestUser', 'test@test.com', '1234', 'Activo', 1))
        
        cursor.execute("DELETE FROM Mensaje WHERE IDUsuario = (SELECT IDUsuario FROM Usuario WHERE Nombre='TestUser')")
        cursor.execute("""
            INSERT INTO Mensaje (IDUsuario, Texto, Fecha) 
            VALUES 
            ((SELECT IDUsuario FROM Usuario WHERE Nombre='TestUser'), 'Capturó un Pikachu', '12/01/2025')
        """)
        
        conn.commit()
        conn.close()



    # 1. PRUEBA DE LISTADO 
    def test_2A_listado_basico(self):
        """Prueba que carga la lista con datos"""
        response = self.client.get('/changelog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pikachu', response.data)

    # 2. PRUEBA DE FEED VACÍO 
    def test_2B_feed_vacio(self):
        """Prueba que sale el mensaje correcto cuando no hay eventos"""
        conn = sqlite3.connect(TEST_DB)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Mensaje")
        conn.commit()
        conn.close()

        response = self.client.get('/changelog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No hay actividad reciente', response.data)

    # 3. PRUEBA DE BOTÓN VOLVER 
    def test_2C_boton_volver(self):
        """Comprueba que existe un enlace o botón para volver atrás"""
        response = self.client.get('/changelog')
        self.assertEqual(response.status_code, 200)
        # Buscamos la imagen de la flecha 'return.png' que pusimos
        self.assertIn(b'return.png', response.data)

    # 4. PRUEBA DE FILTRO BUSCAR POSITIVO 
    def test_4D_buscar_usuario_existente(self):
        """Busca un usuario que sí existe"""
        response = self.client.post('/changelog', data={'busqueda': 'TestUser'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pikachu', response.data)

    # 5. PRUEBA DE FILTRO BUSCAR NEGATIVO 
    def test_4D_buscar_usuario_inexistente(self):
        """Busca un usuario que NO existe"""
        response = self.client.post('/changelog', data={'busqueda': 'Gaspar'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Pikachu', response.data)

    # 6. PRUEBA DE BOTÓN TODOS 
    def test_4A_boton_todos(self):
        """Prueba que al volver a cargar la página sin búsqueda, sale todo"""
        self.client.post('/changelog', data={'busqueda': 'Gaspar'})
        response = self.client.get('/changelog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pikachu', response.data)

if __name__ == '__main__':
    unittest.main()