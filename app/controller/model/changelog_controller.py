from datetime import datetime

class ChangelogController:
    def __init__(self, db):
        self.db = db

    def agregar_mensaje(self, id_usuario, texto):
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.db.insert(
                "INSERT INTO Mensaje (Fecha, IDUsuario, Texto) VALUES (?, ?, ?)",
                [fecha_actual, id_usuario, texto]
            )
            return True
        except Exception as e:
            print(f"[MODELO] Error al insertar mensaje: {e}")
            return False

    def obtener_todos_mensajes(self):
        sql = """
            SELECT m.Fecha, m.Texto, u.Nombre as NombreUsuario, e.Sprite
            FROM Mensaje m
            JOIN Usuario u ON m.IDUsuario = u.IDUsuario
            LEFT JOIN Especie e ON u.IDFavorito = e.PokedexID
            ORDER BY m.Fecha DESC
        """
        return self.db.select(sql)

    def filtrar_mensajes_por_usuario(self, nombre_usuario):
        sql = """
            SELECT m.Fecha, m.Texto, u.Nombre as NombreUsuario, e.Sprite
            FROM Mensaje m
            JOIN Usuario u ON m.IDUsuario = u.IDUsuario
            LEFT JOIN Especie e ON u.IDFavorito = e.PokedexID
            WHERE u.Nombre LIKE ?
            ORDER BY m.Fecha DESC
        """
        return self.db.select(sql, [f"%{nombre_usuario}%"])

    def esta_vacio(self):
        rows = self.db.select("SELECT count(*) as total FROM Mensaje")
        return rows[0]["total"] == 0