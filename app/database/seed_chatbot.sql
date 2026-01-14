-- =========================
-- SEED MÍNIMO PARA CHATBOT
-- =========================
-- Objetivo:
--  - /stats: Pokemon con stats en tabla Pokemon
--  - /compare: 2 pokemon con stats
--  - /score_team: 1 equipo del admin con 3 pokemon
--  - /weaknesses: Tipos + Debil + REspecieTipo para bulbasaur
--  - /evolution: Cadena bulbasaur -> ivysaur -> venusaur
--  - Casos "caracteres especiales": porygon-z

-- Asegurar admin (por si schema no lo inserta o se reinicia la BD)
INSERT OR IGNORE INTO Usuario (IDUsuario, Nombre, Email, Contrasena, Estado, IDFavorito)
VALUES (1, 'admin', 'admin@admin.com', 'admin', 'Admin', 1);

-- =========================
-- ESPECIES (mínimas)
-- =========================
INSERT OR IGNORE INTO Especie
(PokedexID, Nombre, EsLegendario, Generacion, Sprite, NombreItem, Descripcion, Altura, Peso, Categoria, TieneEvolucion, Prevolucion)
VALUES
(1,   'bulbasaur', 0, 1, 'None', 'None', 'Seed', 7.0, 69.0,  'Seed', 1, NULL),
(2,   'ivysaur',   0, 1, 'None', 'None', 'Seed', 10.0, 130.0,'Seed', 1, 1),
(3,   'venusaur',  0, 1, 'None', 'None', 'Seed', 20.0, 1000.0,'Seed',0, 2),
(25,  'pikachu',   0, 1, 'None', 'None', 'Seed', 4.0, 60.0, 'Seed', 0, NULL),
(474, 'porygon-z', 0, 4, 'None', 'None', 'Seed', 9.0, 34.0, 'Seed', 0, NULL);

-- =========================
-- TIPOS + RELACIONES ESPECIE-TIPO
-- =========================
INSERT OR IGNORE INTO Tipo (Nombre) VALUES
('planta'), ('veneno'), ('electrico'),
('fuego'), ('hielo'), ('volador'), ('psiquico'),
('agua'), ('hada'), ('normal');

-- Bulbasaur: planta + veneno
INSERT OR IGNORE INTO REspecieTipo (NombreTipo, PokedexID) VALUES
('planta', 1),
('veneno', 1);

-- Pikachu: electrico
INSERT OR IGNORE INTO REspecieTipo (NombreTipo, PokedexID) VALUES
('electrico', 25);

-- Porygon-Z: normal (por simplificar)
INSERT OR IGNORE INTO REspecieTipo (NombreTipo, PokedexID) VALUES
('normal', 474);

-- =========================
-- DEBILIDADES (mínimas para que /weaknesses tenga salida)
-- Debil(NombreTipoDebil, NombreTipoFuerte)
-- -> "TipoDebil" es el del pokemon, "TipoFuerte" es el que le hace daño
-- =========================
INSERT OR IGNORE INTO Debil (NombreTipoDebil, NombreTipoFuerte) VALUES
('planta', 'fuego'),
('planta', 'hielo'),
('planta', 'volador'),
('veneno', 'psiquico');

-- Para "fortalezas" (tu código las calcula como el inverso: NombreTipoFuerte = tipoPokemon)
-- o sea: si planta es fuerte contra agua, entonces (agua, planta)
INSERT OR IGNORE INTO Debil (NombreTipoDebil, NombreTipoFuerte) VALUES
('agua', 'planta'),
('hada', 'veneno');

-- =========================
-- POKEMON (con stats)  (tabla Pokemon)
-- =========================
-- (IDPokemon AUTOINCREMENT) -> dejamos que se genere
INSERT OR IGNORE INTO Pokemon
(Nombre, Nivel, PS, Ataque, AtaqueEspecial, Defensa, DefensaEspecial, Velocidad, IDEspecie)
VALUES
('bulbasaur', 5, 45, 49, 65, 49, 65, 45, 1),
('pikachu',   5, 35, 55, 50, 40, 50, 90, 25),
('porygon-z',  5, 85, 80, 135, 70, 75, 90, 474);

-- =========================
-- EQUIPO DEMO + RELACIÓN EQUIPO-POKEMON
-- =========================
INSERT OR IGNORE INTO Equipo (IDEquipo, Nombre, IDUsuario)
VALUES (1, 'EquipoDemo', 1);

-- Meter 3 pokémon al equipo: bulbasaur, pikachu, porygon-z
INSERT OR IGNORE INTO REquipoPokemon (IDEquipo, IDPokemon, Slot)
SELECT 1, p.IDPokemon, 1 FROM Pokemon p WHERE p.Nombre='bulbasaur';

INSERT OR IGNORE INTO REquipoPokemon (IDEquipo, IDPokemon, Slot)
SELECT 1, p.IDPokemon, 2 FROM Pokemon p WHERE p.Nombre='pikachu';

INSERT OR IGNORE INTO REquipoPokemon (IDEquipo, IDPokemon, Slot)
SELECT 1, p.IDPokemon, 3 FROM Pokemon p WHERE p.Nombre='porygon-z';
