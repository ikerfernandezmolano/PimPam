import sqlite3
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
            SELECT
                rep.Slot,
                p.IDPokemon,
                p.Nombre,
                e.Sprite AS Sprite
            FROM REquipoPokemon rep
            JOIN Pokemon p ON p.IDPokemon = rep.IDPokemon
            JOIN Especie e ON e.PokedexID = p.IDEspecie
            WHERE rep.IDEquipo = ?
            ORDER BY rep.Slot
            """,
            (idEquipo,)
        )

    def getPokedex(self):
        return self.db.select(
            """
            SELECT
                p.IDPokemon,
                p.Nombre
            FROM Pokemon p
            """
        )

    def saveNewEquipo(self, idUsuario, nombre):
        equipos = self.getEquiposUsuario(idUsuario)

        if any(e['Nombre'] == nombre for e in equipos):
            return None

        try:
            return self.db.insert(
                "INSERT INTO Equipo (Nombre, IDUsuario) VALUES (?, ?)",
                (nombre, idUsuario)
            )
        except sqlite3.IntegrityError:
            return None



        return fila[0]["id"]

    def insertPokemon(self, idEquipo, idPokemon, slot):
        try:
            self.db.insert(
                "INSERT INTO REquipoPokemon (IDEquipo, IDPokemon, Slot) VALUES (?, ?, ?)",
                (idEquipo, idPokemon, slot)
            )
        except sqlite3.IntegrityError:
            return


    def deletePokemon(self, idEquipo, slot):
        self.db.delete(
            """
            DELETE FROM REquipoPokemon
            WHERE IDEquipo = ? AND Slot = ?
            """,
            (idEquipo, slot)
        )

    def deleteEquipo(self, idEquipo, slot=None):
        if slot is not None:
            self.db.delete(
                "DELETE FROM REquipoPokemon WHERE IDEquipo = ? AND Slot = ?",
                (idEquipo, slot)
            )
        else:
            self.db.delete(
                "DELETE FROM REquipoPokemon WHERE IDEquipo = ?",
                (idEquipo,)
            )
            self.db.delete(
                "DELETE FROM Equipo WHERE IDEquipo = ?",
                (idEquipo,)
            )

    def reemplazarPokemon(self, idEquipo, slot, idPokemon):
        pokemons = self.getPokemonEquipo(idEquipo)
        self.deletePokemon(idEquipo, slot)
        if len(pokemons) >=6 and slot >=len(pokemons):
            return
        self.insertPokemon(idEquipo, idPokemon, slot)

    def saveNewNombre(self, idEquipo, nuevoNombre):
        self.db.update(
            "UPDATE Equipo SET Nombre = ? WHERE IDEquipo = ?",
            (nuevoNombre, idEquipo)
        )

    def getEquipoPorNombre(self, nombre_equipo: str):
        rows = self.db.select(
            "SELECT IDEquipo, Nombre FROM Equipo WHERE LOWER(Nombre) = LOWER(?) LIMIT 1",
            [nombre_equipo]
        )
        return dict(rows[0]) if rows else None