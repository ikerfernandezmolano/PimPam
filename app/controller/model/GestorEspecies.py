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
        res = self.db.select("SELECT COUNT(*) AS TOTAL FROM Especie")
        if res and res[0]["TOTAL"]==0:
            for i in range(1, limit):
                p = pb.pokemon(i)
                e = pb.pokemon_species(i)
                self.db.insert("INSERT INTO Especie VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",[p.id,p.name,e.is_legendary, e.generation.url.rstrip('/').split('/')[-1],p.sprites.front_default,"Prueba","Prueba",p.height,p.weight,"Prueba",1,1])

    def get_all(self):
        rows = self.db.select("SELECT * FROM Especie")
        return [dict(row) for row in rows]

    def getPokemonPorNombre(self, nombre: str):
        rows = self.db.select(
            "SELECT * FROM Pokemon WHERE LOWER(Nombre) = LOWER(?) LIMIT 1",
            [nombre]
        )
        if not rows:
            return None
        return dict(rows[0])
