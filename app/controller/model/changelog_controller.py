from datetime import datetime

class ChangelogController:
    """
    Controlador encargado de gestionar la lógica de negocio del Changelog.
    Realiza las operaciones CRUD contra la base de datos relacionadas con los mensajes y notificaciones.
    """
    def __init__(self, db):
        # Recibimos la instancia de la base de datos para ejecutar consultas
        self.db = db

    def agregar_mensaje(self, id_usuario, texto):
        """
        Registra un nuevo evento en el historial.
        """
        # Obtenemos la fecha y hora actual en formato compatible con SQL
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            # Insertamos el mensaje vinculándolo al ID del usuario que realizó la acción
            self.db.insert(
                "INSERT INTO Mensaje (Fecha, IDUsuario, Texto) VALUES (?, ?, ?)",
                [fecha_actual, id_usuario, texto]
            )
            return True
        except Exception as e:
            # Manejo de errores: si falla la inserción, lo registramos en consola pero no rompemos la app
            print(f"[MODELO] Error al insertar mensaje: {e}")
            return False

    def obtener_todos_mensajes(self):
        """
        Recupera el historial completo de mensajes para mostrar el feed general.
        Realiza un JOIN con la tabla Usuario y Especie para obtener nombres e imágenes.
        """
        sql = """
            SELECT m.Fecha, m.Texto, u.Nombre as NombreUsuario, e.Sprite
            FROM Mensaje m
            JOIN Usuario u ON m.IDUsuario = u.IDUsuario
            LEFT JOIN Especie e ON u.IDFavorito = e.PokedexID
            ORDER BY m.Fecha DESC
        """
        # Ejecutamos la consulta sin parámetros (trae todo)
        return self.db.select(sql)

    def filtrar_mensajes_por_usuario(self, nombre_usuario):
        """
        Filtra los mensajes buscando coincidencias en el nombre del usuario.
        """
        sql = """
            SELECT m.Fecha, m.Texto, u.Nombre as NombreUsuario, e.Sprite
            FROM Mensaje m
            JOIN Usuario u ON m.IDUsuario = u.IDUsuario
            LEFT JOIN Especie e ON u.IDFavorito = e.PokedexID
            WHERE u.Nombre LIKE ?
            ORDER BY m.Fecha DESC
        """
        # Usamos LIKE con porcentajes para búsquedas parciales (ej: "Ash" encuentra "AshKetchum")
        return self.db.select(sql, [f"%{nombre_usuario}%"])

    def esta_vacio(self):
        """
        Método auxiliar para verificar si la tabla de mensajes está vacía.
        Útil para mostrar mensajes de bienvenida o estados vacíos.
        """
        rows = self.db.select("SELECT count(*) as total FROM Mensaje")
        return rows[0]["total"] == 0