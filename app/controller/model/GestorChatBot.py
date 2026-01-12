from app.controller.model.Sesion import Sesion


class GestorChatBot:
    def __init__(self, gestor_especies, gestor_equipos):
        self.gestor_especies = gestor_especies
        self.gestor_equipos = gestor_equipos

        # comandos soportados y nº de argumentos
        self.comandos = {
            "/stats": 1,
            "/weaknesses": 1,
            "/evolution": 1,
            "/score_team": 1,
            "/compare": 2
        }

    def procesarComando(self, pComando: str) -> str:
        comando = (pComando or "").strip()

        # 1) vacío
        if not comando:
            return "No se puede enviar un mensaje vacío."

        # 2) debe empezar por /
        if not comando.startswith("/"):
            return "Error de sintaxis. Falta el icono de inicio de comando '/'."

        partes = comando.split()
        cmd = partes[0]
        args = partes[1:]

        if cmd == "/":
            return "Error de sintaxis. Falta el comando."

        # 3) comando existe
        if cmd not in self.comandos:
            return "Error de sintaxis. Comando no encontrado."

        # 4) nº de argumentos correcto
        n_req = self.comandos[cmd]
        if len(args) < n_req:
            # el enunciado distingue a veces "Falta el argumento" vs "Falta un argumento"
            # dejamos uno genérico y válido
            return "Error de sintaxis. Falta el argumento."
        if len(args) > n_req:
            return "Error de sintaxis. Demasiados argumentos."

        # 5) enrutar
        try:
            if cmd == "/stats":
                return self._cmd_stats(args[0])

            if cmd == "/weaknesses":
                return self._cmd_weaknesses(args[0])

            if cmd == "/evolution":
                return self._cmd_evolution(args[0])

            if cmd == "/compare":
                return self._cmd_compare(args[0], args[1])

            if cmd == "/score_team":
                return self._cmd_score_team(args[0])

            return "Error interno."
        except Exception:
            # mínimo correcto: nunca debe petar el sistema
            return "Error interno. Inténtalo más tarde."

    # --------------------
    # Implementación real
    # --------------------

    def _cmd_stats(self, nombre_pokemon: str) -> str:
        p = self.gestor_especies.getPokemonPorNombre(nombre_pokemon)
        if not p:
            return "Pokémon no encontrado."

        return (
            f"{p.get('Nombre')} "
            f"(PS {p.get('PS')}, Atq {p.get('Ataque')}, Def {p.get('Defensa')}, "
            f"AtqEsp {p.get('AtaqueEspecial')}, DefEsp {p.get('DefensaEspecial')}, "
            f"Vel {p.get('Velocidad')})."
        )

    def _cmd_compare(self, p1: str, p2: str) -> str:
        a = self.gestor_especies.getPokemonPorNombre(p1)
        b = self.gestor_especies.getPokemonPorNombre(p2)

        if not a or not b:
            return "Pokémon no encontrado."

        def total_stats(pk):
            return sum([
                pk.get("PS") or 0,
                pk.get("Ataque") or 0,
                pk.get("Defensa") or 0,
                pk.get("AtaqueEspecial") or 0,
                pk.get("DefensaEspecial") or 0,
                pk.get("Velocidad") or 0,
            ])

        ta = total_stats(a)
        tb = total_stats(b)

        if ta > tb:
            ganador = a.get("Nombre")
        elif tb > ta:
            ganador = b.get("Nombre")
        else:
            ganador = "Empate"

        return (
            f"Comparación {a.get('Nombre')} vs {b.get('Nombre')}: "
            f"Total {ta} vs {tb}. Resultado: {ganador}."
        )

    def _cmd_weaknesses(self, especie: str) -> str:
        # Esto depende de tablas Tipo/Debil/REspecieTipo.
        # Si no están pobladas, devolvemos respuesta controlada.
        info = self.gestor_especies.getDebilidadesYFortalezasPorEspecie(especie)
        if info is None:
            return "Pokémon no encontrado."

        tipos = info.get("tipos", [])
        deb = info.get("debilidades", [])
        fort = info.get("fortalezas", [])

        # Si no hay tipos en BD, respuesta mínima y coherente
        if not tipos:
            return f"{especie}: No hay datos de tipos en la base de datos."

        return (
            f"{especie} (Tipos: {', '.join(tipos)}). "
            f"Débil contra: {', '.join(deb) if deb else 'Ninguno'}. "
            f"Fuerte contra: {', '.join(fort) if fort else 'Ninguno'}."
        )

    def _cmd_evolution(self, especie: str) -> str:
        cadena = self.gestor_especies.getCadenaEvolutivaPorEspecie(especie)
        if cadena is None:
            return "Pokémon no encontrado."

        if not cadena:
            return "No tiene cadena evolutiva."

        return "Cadena evolutiva: " + " -> ".join(cadena)

    def _cmd_score_team(self, nombre_equipo: str) -> str:
        sesion = Sesion().getSession()
        if not sesion:
            return "Debes iniciar sesión para usar este comando."

        id_usuario = sesion.get("IDUsuario")
        if not id_usuario:
            return "Debes iniciar sesión para usar este comando."

        equipos = self.gestor_equipos.getEquiposUsuario(id_usuario) or []
        equipo = None
        for e in equipos:
            if (e.get("Nombre") or "").lower() == nombre_equipo.lower():
                equipo = e
                break

        if not equipo:
            return "Equipo no encontrado."

        pokes = self.gestor_equipos.getPokemonEquipo(equipo["IDEquipo"]) or []
        if not pokes:
            return f"El equipo '{equipo.get('Nombre')}' está vacío."

        # Para evaluar el equipo según stats, buscamos cada Pokémon en tabla Pokemon
        total = 0
        n = 0
        for pk in pokes:
            nombre_pk = pk.get("Nombre")
            if not nombre_pk:
                continue
            stats = self.gestor_especies.getPokemonPorNombre(nombre_pk)
            if not stats:
                continue

            total += sum([
                stats.get("PS") or 0,
                stats.get("Ataque") or 0,
                stats.get("Defensa") or 0,
                stats.get("AtaqueEspecial") or 0,
                stats.get("DefensaEspecial") or 0,
                stats.get("Velocidad") or 0,
            ])
            n += 1

        if n == 0:
            return f"No hay estadísticas disponibles para evaluar el equipo '{equipo.get('Nombre')}'."

        media = total // n
        return (
            f"Equipo '{equipo.get('Nombre')}' evaluado: "
            f"{n} Pokémon, puntuación total {total}, media {media}."
        )
