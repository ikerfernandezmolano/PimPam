import os
from pokebase import cache
import pokebase as pb

os.environ["POKEBASE_DB"] = "dumb"

# Delete old cache to avoid dbm.gnu issues
if os.path.exists(cache.API_CACHE):
    os.remove(cache.API_CACHE)

class GestorEspecies:
    def __init__(self, db):
        self.db = db

    def initialize(self, limit=10):
        """
        Carga inicial mínima desde PokéAPI SOLO si la tabla Especie está vacía.
        Importante: NO inventamos evoluciones aquí (TieneEvolucion=0, Prevolucion=NULL),
        porque si no la cadena evolutiva queda mal.
        """
        res = self.db.select("SELECT COUNT(*) AS TOTAL FROM Especie")
        if res and res[0]["TOTAL"] == 0:
            for i in range(1, limit):
                p = pb.pokemon(i)
                e = pb.pokemon_species(i)
                self.db.insert(
                    "INSERT INTO Especie VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    [
                        p.id,
                        p.name,
                        e.is_legendary,
                        e.generation.url.rstrip("/").split("/")[-1],
                        p.sprites.front_default,
                        "Prueba",
                        "Prueba",
                        p.height,
                        p.weight,
                        "Prueba",
                        0,      # TieneEvolucion (mínimo seguro)
                        None    # Prevolucion (mínimo seguro)
                    ],
                )
        return self  # útil para llamadas tipo GestorEspecies(...).initialize()

    def get_all(self):
        rows = self.db.select("SELECT * FROM Especie")
        return [dict(row) for row in rows]

    def getPokemonPorNombre(self, nombre: str):
        rows = self.db.select(
            "SELECT * FROM Pokemon WHERE LOWER(Nombre) = LOWER(?) LIMIT 1",
            [nombre],
        )
        if not rows:
            return None
        return dict(rows[0])

    def getEspeciePorNombre(self, nombre: str):
        rows = self.db.select(
            "SELECT * FROM Especie WHERE LOWER(Nombre) = LOWER(?) LIMIT 1",
            [nombre],
        )
        return dict(rows[0]) if rows else None

    def getTiposPorNombreEspecie(self, nombre_especie: str):
        rows = self.db.select(
            """
            SELECT t.Nombre AS Tipo
            FROM Especie e
            JOIN REspecieTipo ret ON ret.PokedexID = e.PokedexID
            JOIN Tipo t ON t.Nombre = ret.NombreTipo
            WHERE LOWER(e.Nombre) = LOWER(?)
            """,
            [nombre_especie],
        )
        return [r["Tipo"] for r in rows] if rows else []

    def getDebilidadesYFortalezasPorEspecie(self, nombre_especie: str):
        e = self.getEspeciePorNombre(nombre_especie)
        if not e:
            return None

        tipos = self.getTiposPorNombreEspecie(nombre_especie)

        debiles = set()
        fuertes = set()

        for t in tipos:
            rows = self.db.select(
                "SELECT NombreTipoFuerte AS T FROM Debil WHERE NombreTipoDebil = ?",
                [t],
            )
            for r in rows:
                debiles.add(r["T"])

            rows = self.db.select(
                "SELECT NombreTipoDebil AS T FROM Debil WHERE NombreTipoFuerte = ?",
                [t],
            )
            for r in rows:
                fuertes.add(r["T"])

        return {
            "tipos": tipos,
            "debilidades": sorted(debiles),
            "fortalezas": sorted(fuertes),
        }

    def getCadenaEvolutivaPorEspecie(self, nombre_especie: str):
        e = self.getEspeciePorNombre(nombre_especie)
        if not e:
            return None

        if not e.get("TieneEvolucion"):
            return []

        especie_id = e["PokedexID"]

        # subir hacia preevolución (con protección anti-bucle)
        ids = []
        actual = especie_id
        visitados = set()

        while True:
            if actual in visitados:
                break
            visitados.add(actual)
            ids.append(actual)

            prev = self.db.select(
                "SELECT Prevolucion FROM Especie WHERE PokedexID = ? LIMIT 1",
                [actual],
            )
            if not prev:
                break

            pre = prev[0]["Prevolucion"]
            if pre is None or pre == actual:
                break

            actual = pre

        ids = list(reversed(ids))

        # bajar hacia evoluciones (si hay varias ramas, cogemos la primera)
        actual = especie_id
        visitados = set(ids)

        while True:
            nxt = self.db.select(
                "SELECT PokedexID FROM Especie WHERE Prevolucion = ? LIMIT 1",
                [actual],
            )
            if not nxt:
                break

            actual = nxt[0]["PokedexID"]
            if actual in visitados:
                break
            visitados.add(actual)
            ids.append(actual)

        # ids -> nombres
        nombres = []
        for pid in ids:
            r = self.db.select(
                "SELECT Nombre FROM Especie WHERE PokedexID = ? LIMIT 1",
                [pid],
            )
            if r:
                nombres.append(r[0]["Nombre"])

        return [] if len(nombres) <= 1 else nombres
