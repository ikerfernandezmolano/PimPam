class GestorEquipos:
    def __init__(self, db):
        self.db = db

    def getEquiposUsuario(self, idUsuario):
        return self.db.select(
            "SELECT IDEquipo, Nombre FROM Equipo WHERE IDUsuario = ?",
            [idUsuario]
        )

    def getPokemonEquipo(self, idEquipo):
        return self.db.select(
            """
            SELECT p.IDPokemon, p.Nombre, e.Sprite, rep.Slot
            FROM REquipoPokemon rep
            JOIN Pokemon p ON p.IDPokemon = rep.IDPokemon
            JOIN Especie e ON e.PokedexID = p.IDEspecie
            WHERE rep.IDEquipo = ?
            ORDER BY rep.Slot
            """,
            [idEquipo]
        )

    def getPokedex(self):
        return self.db.select(
            "SELECT IDPokemon, Nombre FROM Pokemon ORDER BY Nombre"
        )

    def crearEquipo(self, idUsuario, nombre):
        self.db.insert(
            "INSERT INTO Equipo (Nombre, IDUsuario) VALUES (?, ?)",
            [nombre, idUsuario]
        )

    def eliminarEquipo(self, idEquipo):
        self.db.insert(
            "DELETE FROM REquipoPokemon WHERE IDEquipo = ?",
            [idEquipo]
        )
        self.db.insert(
            "DELETE FROM Equipo WHERE IDEquipo = ?",
            [idEquipo]
        )

    def insertarPokemon(self, idEquipo, idPokemon, slot):
        self.db.insert(
            """
            INSERT INTO REquipoPokemon (IDEquipo, IDPokemon, Slot)
            VALUES (?, ?, ?)
            """,
            [idEquipo, idPokemon, slot]
        )

    def eliminarPokemon(self, idEquipo, slot):
        self.db.insert(
            """
            DELETE FROM REquipoPokemon
            WHERE IDEquipo = ? AND Slot = ?
            """,
            [idEquipo, slot]
        )

    def reemplazarPokemon(self, idEquipo, slot, idPokemon):
        self.eliminarPokemon(idEquipo, slot)
        self.insertarPokemon(idEquipo, idPokemon, slot)

    def modificarNombreEquipo(self, idEquipo, nuevoNombre):
        self.db.insert(
            "UPDATE Equipo SET Nombre = ? WHERE IDEquipo = ?",
            [nuevoNombre, idEquipo]
        )
