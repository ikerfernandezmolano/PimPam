import unittest
import os
import sqlite3
import sys
import time

sys.path.insert(0, os.getcwd())

from app import create_app
from app.config import Config

TEST_DB = "test_pimpam.db"


class TestChatbotGeneral(unittest.TestCase):
    """
    PRUEBAS GENERALES 3.5.1 (1A-1G)
    - 1A y 1G: manuales (UI)
    - 1B-1F: automáticas (unittest)
    """

    def setUp(self):
        # Borrar DB de tests si existe (Windows a veces la bloquea)
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except PermissionError:
                time.sleep(0.1)
                try:
                    os.remove(TEST_DB)
                except Exception:
                    pass

        # Usar DB de tests
        Config.DB_PATH = TEST_DB

        # Crear app
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Extra seguridad: asegurar schema y seed (idempotente)
        self._ensure_schema_and_seed()

    def tearDown(self):
        self.client = None
        self.app = None

        # Intentar borrar DB de tests
        if os.path.exists(TEST_DB):
            try:
                time.sleep(0.1)
                os.remove(TEST_DB)
            except PermissionError:
                time.sleep(0.2)
                try:
                    os.remove(TEST_DB)
                except Exception:
                    pass

    def _ensure_schema_and_seed(self):
        conn = sqlite3.connect(Config.DB_PATH, timeout=10)
        cur = conn.cursor()

        schema_path = os.path.join(os.getcwd(), "app", "database", "schema.sql")
        with open(schema_path, "r", encoding="utf-8") as f:
            try:
                cur.executescript(f.read())
            except sqlite3.OperationalError:
                pass

        seed_path = os.path.join(os.getcwd(), "app", "database", "seed_chatbot.sql")
        if os.path.exists(seed_path):
            with open(seed_path, "r", encoding="utf-8") as f:
                try:
                    cur.executescript(f.read())
                except sqlite3.OperationalError:
                    pass

        conn.commit()
        conn.close()

    # Helper para llamar al endpoint del chatbot
    def _consultar(self, comando: str) -> str:
        res = self.client.post("/chatbot/consultar", json={"comando": comando})
        self.assertEqual(res.status_code, 200)
        data = res.get_json() or {}
        return data.get("respuesta", "")

    # -------------------------
    # PRUEBAS GENERALES (1A-1G)
    # -------------------------

    # 1A (MANUAL): Acceso al Chatbot desde el menú principal
    # -> Se documenta con captura en la memoria.

    def test_1B_mensaje_vacio_o_espacios(self):
        """
        1B: Mensaje vacío o espacios.
        Salida esperada: "No se puede enviar."
        """
        out1 = self._consultar("")
        self.assertEqual(out1, "No se puede enviar.")

        out2 = self._consultar("   ")
        self.assertEqual(out2, "No se puede enviar.")

    def test_1C_inicio_icono_comando_barra_sola(self):
        """
        1C: Inicio del icono de comando "/".
        Salida esperada: "Error de sintaxis. Falta el comando. Muestra los comandos posibles."
        """
        out = self._consultar("/")
        self.assertIn("Error de sintaxis. Falta el comando. Muestra los comandos posibles.", out)

        # Extra (recomendado): evidencia de que realmente muestra comandos
        self.assertIn("/stats", out)

    def test_1D_comando_inexistente(self):
        """
        1D: Comando inexistente.
        Salida esperada: "Error de sintaxis. Comando no encontrado."
        """
        out = self._consultar("/comandoInventado bulbasaur")
        self.assertEqual(out, "Error de sintaxis. Comando no encontrado.")

    def test_1E_comando_sin_icono_barra(self):
        """
        1E: Comando sin icono de inicio "/".
        Salida esperada: "Error de sintaxis. Falta el icono de inicio de comando '/'."
        """
        out = self._consultar("stats bulbasaur")
        self.assertEqual(out, "Error de sintaxis. Falta el icono de inicio de comando '/'.")

    def test_1F_mensaje_aleatorio(self):
        """
        1F: Mensaje aleatorio.
        Salida esperada: "Error de sintaxis. Falta el icono de inicio de comando '/'."
        """
        out = self._consultar("hola")
        self.assertEqual(out, "Error de sintaxis. Falta el icono de inicio de comando '/'.")

    # 1G (MANUAL): Botón retroceder
    # -> Se documenta con captura en la memoria.


if __name__ == "__main__":
    unittest.main()
