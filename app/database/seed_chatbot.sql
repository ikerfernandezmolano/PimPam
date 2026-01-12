-- =========================
-- SEED MÍNIMO PARA CHATBOT
-- =========================
-- Objetivo:
--  - /stats: Pokemon con stats en tabla Pokemon
--  - /compare: 2 pokemon con stats
--  - /score_team: 1 equipo del admin con 3 pokemon
--  - /weaknesses: Tipos + Debil + REspecieTipo para bulbasaur
--  - /evolution: Cadena bulbasaur -> ivysaur -> venusaur

-- asegurar admin (por si seed se ejecuta en una BD vacía)
INSERT OR IGNORE INTO Usuario (IDUsuario, Nombre, Email, Contrasena, Estado, IDFavorito)
VALUES (1, 'admin', 'admin@admin.com', 'admin', 'Admin', 1);

-- 1) Asegurar especies clave (por si initialize no se ejecutó)
INSERT OR IGNORE INTO Especie
(PokedexID, Nombre, EsLegendario, Generacion, Sprite, NombreItem, Descripcion, Altura, Peso, Categoria, TieneEvolucion, Prevolucion)
VALUES
(1,'bulbasaur',0,1,'None','None','None',7,69,'Seed',1,NULL),
(2,'ivysaur',0,1,'None','None','None',10,130,'Seed',1,1),
(3,'venusaur',0,1,'None','None','None',20,1000,'Seed',0,2),
(6,'charizard',0,1,'None','None','None',17,905,'Seed',0,NULL),
(25,'pikachu',0,1,'None','None','None',4,60,'Seed',0,NULL);

-- 2) Corregir evolución si ya existían (evita bucles / datos malos)
UPDATE Especie SET TieneEvolucion = 1, Prevolucion = NULL WHERE PokedexID = 1;
UPDATE Especie SET TieneEvolucion = 1, Prevolucion = 1    WHERE PokedexID = 2;
UPDATE Especie SET TieneEvolucion = 0, Prevolucion = 2    WHERE PokedexID = 3;

-- 3) Pokémon con stats (tabla Pokemon) para /stats y /compare
-- Ponemos IDs fijos para poder referenciarlos en el equipo.
INSERT OR IGNORE INTO Pokemon
(IDPokemon, Nombre, Nivel, PS, Ataque, AtaqueEspecial, Defensa, DefensaEspecial, Velocidad, IDEspecie)
VALUES
(101,'bulbasaur',5,45,49,65,49,65,45,1),
(102,'ivysaur',16,60,62,80,63,80,60,2),
(103,'venusaur',32,80,82,100,83,100,80,3),
(104,'charizard',36,78,84,109,78,85,100,6),
(105,'pikachu',12,35,55,50,40,50,90,25);

-- 4) Equipo del admin para /score_team
INSERT OR IGNORE INTO Equipo (IDEquipo, Nombre, IDUsuario)
VALUES (900, 'EquipoDemo', 1);

INSERT OR IGNORE INTO REquipoPokemon (IDEquipo, IDPokemon, Slot)
VALUES
(900, 101, 1),
(900, 104, 2),
(900, 105, 3);

-- 5) Tipos / Debilidades / Fortalezas para /weaknesses (bulbasaur)
INSERT OR IGNORE INTO Tipo (Nombre) VALUES
('grass'), ('poison'), ('fire'), ('water'), ('ground'), ('psychic'), ('ice'), ('flying'), ('bug'), ('rock'), ('fairy');

-- Asignar tipos a bulbasaur (Especie 1)
INSERT OR IGNORE INTO REspecieTipo (NombreTipo, PokedexID)
VALUES
('grass', 1),
('poison', 1);

-- Debil: (NombreTipoDebil, NombreTipoFuerte)
-- Débil contra:
INSERT OR IGNORE INTO Debil (NombreTipoDebil, NombreTipoFuerte) VALUES
('grass','fire'),
('grass','ice'),
('grass','flying'),
('grass','bug'),
('poison','psychic'),
('poison','ground');

-- Fuerte contra (para que tu query "NombreTipoFuerte = tipo" funcione):
-- Si grass es fuerte contra water/ground/rock => (water, grass), (ground, grass), (rock, grass)
INSERT OR IGNORE INTO Debil (NombreTipoDebil, NombreTipoFuerte) VALUES
('water','grass'),
('ground','grass'),
('rock','grass'),
('grass','poison'),  -- poison fuerte contra grass => (grass, poison)
('fairy','poison');  -- poison fuerte contra fairy => (fairy, poison)
